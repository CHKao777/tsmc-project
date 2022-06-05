from datetime import date
from crawler.GoogleCrawler import add_new_date

def test_mongodb_log_basic(mongodb):
    assert 'crawler_logs' in mongodb.list_collection_names()
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-01'})
    assert log['Status'] == 'Done'

def test_add_new_date(mongodb):
    assert 'crawler_logs' in mongodb.list_collection_names()

    start_date = date.fromisoformat('2022-06-01')

    add_new_date(mongodb.crawler_logs, 1, start_date)
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-01'})
    assert log
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-03'})
    assert not log

    start_date = date.fromisoformat('2022-06-03')

    add_new_date(mongodb.crawler_logs, 1, start_date)
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-03'})
    assert log
    assert log['Status'] == 'undone'