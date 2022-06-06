from GoogleCrawler import GoogleCrawler
from worker import work

import time
import datetime

from redis import Redis
from rq import Queue
from rq.job import Job



class GoogleCrawlerTest(GoogleCrawler):

    def __init__(self):
        self.url = 'https://www.google.com/search?q=' 
        self.query_list = ['tsmc', 'asml', 'applied materials', 'sumco']

        self.search_interval = 60.0 #兩次google search的間隔時間(秒)
        self.last_search_time = time.time() #gggoogle search的時間

        self.job_result = []

        self.connection = Redis('redis', 6379)
        self.rq = Queue(name='test', connection=self.connection)
        self.rq.empty()

        self.patience = 600
    
    def google_search_one_query(self, query, time_start, time_end, max_search):
        result = []
        for i in range((max_search - 1) // 100 + 1):
            part_result = self.google_search_once(query, time_start, time_end, str(i*100), '100')
            if len(part_result) == 0 or part_result is None:
                break
            # self.enqueue(part_result)
            result += part_result
        print('Get {:d} urls for {:s} from {:s} to {:s}'.format(len(result), query, time_start, time_end),flush=True)
        return result, len(result)
    
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

    def google_search_all_query(self, time_start, time_end, max_search_each_query=1000):
        #initialization
        self.rq.empty()
        self.job_result = []

        url_counts = []
        url_list = []
        for query in self.query_list:
            part_result ,url_count = self.google_search_one_query(query, time_start, time_end, max_search=max_search_each_query)
            url_list += part_result
            json_data = {
                'Date' : time_start,
                'Company' : query, 
                'Url_Count' : url_count
            }
            url_counts.append(json_data)

        start = time.time()
        self.enqueue(url_list)
        for job in self.job_result:
            while not job.is_finished and not job.is_failed:
                time.sleep(0.001)
        end = time.time()
        print('{:d} jobs doned in {:.2f} seconds, throughput:{:.2f}'.format(len(url_list), end - start, len(url_list)/(end - start)))
        
