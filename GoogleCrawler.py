import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
import datetime

from redis import Redis
from rq import Queue
from worker import work

import pymongo


rq = Queue(connection=Redis('redis', 6379))
mongodb_server_hostname = 'mongodb-server'
mongodb_client_connection = 'mongodb://{}:27017/'.format(mongodb_server_hostname)
myclient = pymongo.MongoClient(mongodb_client_connection)
mydb = myclient["tsmc_project"]
collect = mydb['url_count']
crawler_log = mydb['crawler_log']

class GoogleCrawler():
    
    def __init__(self):
        self.url = 'https://www.google.com/search?q=' 
        self.query_list = ['tsmc', 'asml', 'applied materials', 'sumco']
        self.search_interval = 60.0 #兩次google search的間隔時間(秒)
        self.last_search_time = time.time() #上次google search的時間

    def get_source(self,url):
        try:
            session = HTMLSession()
            response = session.get(url, timeout=10)
            return response
        except requests.exceptions.RequestException as e:
            pass
    
    #進行google_serach_once前, 要先確保時間間隔足夠
    def google_search_get_ready(self):
        second_since_last_search = time.time() - self.last_search_time
        if second_since_last_search < self.search_interval:
            print('sleeping...',flush=True)
            time.sleep(self.search_interval - second_since_last_search)

    #進行一次google search
    def google_search_once(self, query, time_start, time_end, serp_start, num):
        self.google_search_get_ready()
        url = self.url + query + ' before:{before} after:{after}&start={serp_start}&num={num}&hl=en'.format(before=time_end, after=time_start, serp_start=serp_start, num=num)
        print('[Check][URL] URL : {url}'.format(url=url),flush=True)
        response = self.get_source(url)
        self.last_search_time = time.time()
        return self.parse_googleResults(response, time_start)
    
    def enqueue(self, url_list):
        for item in url_list:
            rq.enqueue(work, item['url'], item['timestamp'])

    #針對一個query搜尋url, 最大搜尋數量=max_search(總數通常都不會超過1000)
    def google_search_one_query(self, query, time_start, time_end, max_search):
        result = []
        for i in range((max_search - 1) // 100 + 1):
            part_result = self.google_search_once(query, time_start, time_end, str(i*100), '100')
            if len(part_result) == 0 or part_result is None:
                break
            self.enqueue(part_result)
            result += part_result
        print('Get {:d} urls for {:s} from {:s} to {:s}'.format(len(result), query, time_start, time_end),flush=True)
        return result
    
    #對所有query搜尋url, 每個query的最大搜尋數量=max_search_each_query(總數通常都不會超過1000)
    def google_search_all_query(self, time_start, time_end, max_search_each_query=1000):
        for query in self.query_list:
            url_count = len(self.google_search_one_query(query, time_start, time_end, max_search=max_search_each_query))
            json_data = {
                'Date' : time_start,
                'Company' : query, 
                'Url_Count' : url_count,
            }
            collect.insert_one(json_data)

    def parse_googleResults(self, response, timestamp):
        if response is None:
            return None
        css_identifier_result = "tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = "yuRUbf"
        css_identifier_text = "VwiC3b"
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll("div", {"class": css_identifier_result})
        output = []
        for result in results:
            try:
                item = {
                    'url': result.find("div", {"class": css_identifier_link}).find(href=True)['href'],
                    'timestamp': timestamp
                }
                output.append(item)
            except AttributeError as e:
                continue
        return output


if __name__ == '__main__':
    crawler = GoogleCrawler()

    while True:
        job = crawler_log.find_one({'Status': 'undone'})
        if job is None:
            print('nothing to do', flush=True)
            time.sleep(1)
            continue
        crawler_log.update_one({'_id':job['_id']}, {'$set':{'Status':'processing'}})
        start_date = job['Date']
        start_date_object = datetime.datetime.strptime(job['Date'], "%Y-%m-%d")
        end_date_object = datetime.date(start_date_object.year, start_date_object.month, start_date_object.day) + datetime.timedelta(days=6)
        end_date = str(end_date_object)

        try:
            crawler.google_search_all_query(start_date, end_date)
            crawler_log.update_one({'_id':job['_id']}, {'$set':{'Status':'done'}})
        except Exception as e:
            crawler_log.update_one({'_id':job['_id']}, {'$set':{'Status':'undone'}})