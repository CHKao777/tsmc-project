import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import nltk
import pymongo
from redis import Redis
from rq import Queue, Worker
nltk.download('punkt', quiet=True)


keyword_count_dict = {'tsmc': 0, 'asml': 0, 'applied': 0, 'materials': 0, 'sumco': 0}
company_list = ['tsmc', 'asml', 'applied materials', 'sumco']

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb_server_hostname = 'mongodb-server'
mongodb_client_connection = 'mongodb://{}:27017/'.format(mongodb_server_hostname)
myclient = pymongo.MongoClient(mongodb_client_connection)

mydb = myclient["tsmc_project"]
collect = mydb['word_count']

rds = Redis('redis', 6379)
rq = Queue(connection=rds)

def work(url, timestamp):
    response = get_source(url)
    if response is None:
        return None
    soup = html_parser(response.text)
    if soup is None:
        return None
    orignal_text = html_getText(soup)
    company_count(orignal_text, timestamp)

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        pass
    
def html_parser(htmlText):
    try:
        soup = BeautifulSoup(htmlText, 'html.parser')
    except AssertionError as e:
        soup = None
    return soup

def html_getText(soup):
    orignal_text = ''
    for el in soup.find_all('p'):
        orignal_text += ''.join(el.find_all(text=True))
    return orignal_text
    
def company_count(text, timestamp):
    words = word_tokenize(text.lower())
    for word in words:
        if word in keyword_count_dict:
            keyword_count_dict[word] += 1

    for company in company_list:
        if len(company.split()) == 1:
            count = keyword_count_dict[company]
        else:
            count = min(keyword_count_dict[company.split()[0]], keyword_count_dict[company.split()[1]])
        if count == 0:
            continue
        json_data = {
            'Date' : timestamp,
            'Company' : company, 
            'Word_Count' : count,
        }
        collect.insert_one(json_data)
    
if __name__ == '__main__':
    worker = Worker([rq], connection=rds)
    worker.work()