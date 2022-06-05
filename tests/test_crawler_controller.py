from datetime import date


def test_mongodb_log_basic(mongodb):
    assert 'crawler_logs' in mongodb.list_collection_names()
    log = mongodb.crawler_logs.find_one({'Date': '2022-06-01'})
    assert log['Status'] == 'Done'
