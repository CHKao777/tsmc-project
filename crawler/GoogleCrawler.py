import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
import datetime

from redis import Redis
from rq import Queue
from rq.job import Job
from worker import work

import pymongo


class GoogleCrawler():

    def __init__(self):
        self.url = 'https://www.google.com/search?q=' 
        self.query_list = ['tsmc', 'asml', 'applied materials', 'sumco']

        self.search_interval = 60.0 #兩次google search的間隔時間(秒)
        self.last_search_time = time.time() #gggoogle search的時間

        self.job_result = []

        self.connection = Redis('redis', 6379)
        self.rq = Queue(connection=self.connection)
        self.rq.empty()

        myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.mydb = myclient['tsmc_project']
        self.url_counts_collection = self.mydb['url_counts']
        self.word_counts_collection = self.mydb['word_counts']

        self.patience = 600

    def get_source(self, url):
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
        url = self.url + query + \
            ' before:{:s} after:{:s}&start={:s}&num={:s}&hl=en'.format(time_end, time_start, serp_start, num)
        print('[Check][URL] URL : {url}'.format(url=url),flush=True)
        response = self.get_source(url)
        self.last_search_time = time.time()
        return self.parse_googleResults(response, time_start)
    
    #將url_list內的url打包成job, 並enqueue到redis queue, 並在job的結果存於self.job_result
    def enqueue(self, url_list):
        for item in url_list:
            job = Job.create(
                func=work, 
                args=[item['url'], item['timestamp']], 
                connection=self.connection, 
                result_ttl=86400,
                timeout=15,
            )
            self.rq.enqueue_job(job)
            self.job_result.append(job)
    
    #檢查self.job_result內的job是否都完成,並將job的執行結果回傳
    def collect_result(self):
        company_count_dict = {'tsmc': 0, 'asml': 0, 'applied materials': 0, 'sumco': 0}
        start_timestamp = time.time()
        for job in self.job_result:
            while not job.is_finished and not job.is_failed:
                if time.time() - start_timestamp > self.patience:
                    return None
                print('waiting job to be done... check whether workers are '\
                    'running correctly if stucked for a long time', flush=True)
                time.sleep(0.5)
            if job.result:
                for item in job.result:
                    company_count_dict[item['Company']] += item['Word_Count']
        return company_count_dict

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
        return len(result)
    
    #對所有query搜尋url, 每個query的最大搜尋數量=max_search_each_query(總數通常都不會超過1000)
    def google_search_all_query(self, time_start, time_end, max_search_each_query=1000):
        #initialization
        self.rq.empty()
        self.job_result = []

        url_counts = []
        for query in self.query_list:
            url_count = self.google_search_one_query(query, time_start, time_end, max_search=max_search_each_query)
            json_data = {
                'Date' : time_start,
                'Company' : query, 
                'Url_Count' : url_count
            }
            url_counts.append(json_data)

        company_count_dict = self.collect_result()
        if company_count_dict is None:
            print('google_search_all_query on {:s} is failed. word_counts and '\
                'url_counts will not be save to db.'.format(time_start), flush=True)
            return False
        
        print('google_search_all_query on {:s} succeeds. word_counts and '\
            'url_counts will be save to db.'.format(time_start), flush=True)
            
        #save word_counts_total and url_counts to db
        for company, word_count in company_count_dict.items():
            json_data = {
                'Date' : time_start,
                'Company' : company, 
                'Word_Count' : word_count
            }
            self.word_counts_collection.insert_one(json_data)

        for item in url_counts:
            self.url_counts_collection.insert_one(item)
        
        return True

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


def add_new_date(crawler_logs_collection, num_week, start_date):
    for _ in range(num_week):
        x = crawler_logs_collection.find_one({'Date': str(start_date)})
        if x is None:
            json_data = {
                'Date': str(start_date),
                'Status': 'undone'
            }
            crawler_logs_collection.insert_one(json_data)
            print('add {:s} to collection crawler_logs, status:undone '.format(str(start_date)), flush=True)
        start_date -= datetime.timedelta(days=7)


if __name__ == '__main__':
    crawler = GoogleCrawler()

    crawler_logs_collection = crawler.mydb['crawler_logs']

    start_date = datetime.date.today() - \
        datetime.timedelta(days = 7 + datetime.date.today().weekday())
    add_new_date(crawler_logs_collection, 30, start_date)

    while True:
        job = crawler_logs_collection.find_one({'Status': 'undone'})
        if job is None:
            print('all jobs are done, exit crawler', flush=True)
            break

        start_date = job['Date']
        start_date_object = datetime.datetime.strptime(job['Date'], "%Y-%m-%d")
        end_date_object = datetime.date(start_date_object.year, start_date_object.month, start_date_object.day) + \
            datetime.timedelta(days=6)
        end_date = str(end_date_object)

        if_done = crawler.google_search_all_query(start_date, end_date)
        if if_done:
            crawler_logs_collection.update_one({'_id':job['_id']}, {'$set':{'Status':'done'}})