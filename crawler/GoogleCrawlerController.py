import time
import pymongo
import datetime


myclient = pymongo.MongoClient("mongodb://mongodb-service:27017/")
mydb = myclient['tsmc_project']

def add_new_date(crawler_logs_collection, num_week, start_date):

    if_add_new_date = False
    for _ in range(num_week):
        x = crawler_logs_collection.find_one({'Date': str(start_date)})
        
        if x is None:
            json_data = {
                'Date': str(start_date),
                'Status': 'undone'
            }
            crawler_logs_collection.insert_one(json_data)
            if_add_new_date = True
            print('add {:s}'.format(str(start_date)), flush=True)
        start_date -= datetime.timedelta(days=7)
    if not if_add_new_date:
        print('noting to add', flush=True)


if __name__ == '__main__':
    while True:
        crawler_logs_collection = mydb['crawler_logs']
        start_date = datetime.date.today() - \
        datetime.timedelta(days = 7 + datetime.date.today().weekday())

        add_new_date(crawler_logs_collection, 30, start_date)
        time.sleep(60)