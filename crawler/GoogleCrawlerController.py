import time
import pymongo
import datetime


myclient = pymongo.MongoClient("mongodb://mongodb-service:27017/")
mydb = myclient['tsmc_project']
crawler_logs_collection = mydb['crawler_logs']

def add_new_date(num_week):
    start_date = datetime.date.today() - \
        datetime.timedelta(days = 7 + datetime.date.today().weekday())
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
        add_new_date(30)
        time.sleep(60)