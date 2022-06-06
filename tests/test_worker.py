from crawler.worker import company_count

def test_company_count():
    text = 'tsmc, tsmc, applied materials'
    timestamp = '1'
    res = company_count(text, timestamp)
    assert(len(res) == 2)
    assert(res[0].get('Word_Count') == 2)
    assert(res[1].get('Word_Count') == 1)

    text = 'applied math, applied math, applied math, tsmc, tsmc, applied m'
    timestamp = '1'
    res = company_count(text, timestamp)
    assert(len(res) == 1)
    assert(res[0].get('Word_Count') == 2)

    text = 'applied math, applied math, applied math, tsmc, tsmc, applied m??? applied materials'
    timestamp = '1'
    res = company_count(text, timestamp)
    assert(len(res) == 2)
    assert(res[0].get('Word_Count') == 2)
    assert(res[1].get('Word_Count') == 1)
    
