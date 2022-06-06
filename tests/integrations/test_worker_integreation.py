import pytest
import crawler.worker as cworker


@pytest.mark.integration_test
def test_worker():
    url = 'https://www.taipeitimes.com/News/biz/archives/2022/01/20/2003771688'
    res = cworker.work(url, '0')
    assert(res[0].get('Word_Count') == 4)
    assert(res[1].get('Word_Count') == 7)