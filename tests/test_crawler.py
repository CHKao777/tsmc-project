from datetime import date
import datetime
import crawler.GoogleCrawler as gcrawler


def test_mongodb_log_basic(mongodb):
    assert 'crawler_logs' in mongodb.list_collection_names()
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-01'})
    assert log['Status'] == 'Done'

def test_add_new_date(mongodb):
    assert 'crawler_logs' in mongodb.list_collection_names()

    start_date = date.fromisoformat('2022-06-01')

    gcrawler.add_new_date(mongodb.crawler_logs, 1, start_date)
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-01'})
    assert log
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-03'})
    assert not log

    start_date = date.fromisoformat('2022-06-03')

    gcrawler.add_new_date(mongodb.crawler_logs, 1, start_date)
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-03'})
    assert log
    assert log['Status'] == 'undone'

def test_get_first_weekday_at_last_week():
    day = datetime.date(2022, 6, 4)
    assert gcrawler.get_first_weekday_at_last_week(day) == datetime.date(2022, 5, 23)
    day = datetime.date(2022, 6, 5)
    assert gcrawler.get_first_weekday_at_last_week(day) == datetime.date(2022, 5, 23)
    day = datetime.date(2022, 6, 6)
    assert gcrawler.get_first_weekday_at_last_week(day) == datetime.date(2022, 5, 30)
    day = datetime.date(2022, 6, 7)
    assert gcrawler.get_first_weekday_at_last_week(day) == datetime.date(2022, 5, 30)
    day = datetime.date(2022, 6, 8)
    assert gcrawler.get_first_weekday_at_last_week(day) == datetime.date(2022, 5, 30)
    day = datetime.date(2022, 1, 9)
    assert gcrawler.get_first_weekday_at_last_week(day) == datetime.date(2021, 12, 27)


def test_collect_companies_result():
    job = [{'Date' : '0', 'Company' : 'tsmc', 'Word_Count' : 1}]
    res = gcrawler.collect_word_count(job)
    assert res['tsmc'] == 1