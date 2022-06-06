import crawler.worker as cworker


def test_company_count():
    text = 'tsmc, tsmc, applied materials'
    timestamp = '1'
    res = cworker.company_count(text, timestamp)
    assert(len(res) == 2)
    assert(res[0].get('Word_Count') == 2)
    assert(res[1].get('Word_Count') == 1)

    text = 'applied math, applied math, applied math, tsmc, tsmc, applied m'
    timestamp = '1'
    res = cworker.company_count(text, timestamp)
    assert(len(res) == 1)
    assert(res[0].get('Word_Count') == 2)

    text = 'applied math, applied math, applied math, tsmc, tsmc, applied m??? applied materials'
    timestamp = '1'
    res = cworker.company_count(text, timestamp)
    assert(len(res) == 2)
    assert(res[0].get('Word_Count') == 2)
    assert(res[1].get('Word_Count') == 1)

    # with open('testData/a.txt', 'r') as f:
    #     text = f.read()
    text = """
    Intel Corp yesterday said it has placed its first order with ASML Holding NV to purchase the semiconductor industry’s first TWINSCAN EXE: 5200 system, as the US chip giant aims to compete with Taiwan Semiconductor Manufacturing Co (TSMC, 台積電) in advancing to 2-nanometer process technology.
The Dutch semiconductor equipment maker’s TWINSCAN EXE:5200 system is an extreme ultraviolet (EUV) high-volume production system with a high numerical aperture (NA) that can produce 220 wafers per hour, more than the 150 wafers that its previous generation TWINSCAN EXE:5000 system can handle. 
ASML aims to launch the new system in 2024. 
Photo: ReutersASML president and chief technology officer Martin van den Brink said in a statement that the new system “delivers continued lithographic improvements at reduced complexity, cost, cycle time and energy that the chip industry needs to drive affordable scaling well into the next decade.”
Announcing the deal in a statement, Intel executive vice president and general manager of technology development Ann Kelleher said: “Working closely with ASML, we will harness high-NA EUV’s high-resolution patterning as one of the ways we continue Moore’s Law and maintain our strong history of progression down to the smallest of geometries.”
Intel was the first to purchase the TWINSCAN EXE:5000 system in 2018. 
The company said that the new purchase reflects its continued collaboration with ASML and marks the beginning of its production with the new technology in 2025.
TSMC is also likely to buy the TWINSCAN EXE:5200 system and is expected to be the first in the industry to introduce 2-nanometer production, a supply chain source told the Taipei Times yesterday. 
“Placing the first order does not mean Intel will be the first to massively produce chips with the tool,” the source said, adding that Intel still has a long way to go before catching up with TSMC in commercializing 2-nanometer technology.
TSMC’s 2-nanometer chips would enter the market in 2025, the firm said, adding that the chips would be the highest-performing chips available.
Separately, ASML yesterday said that it did not expect a factory fire in Germany to disrupt output.
The fire at its Berlin facility early this month was extinguished within two hours, and the company still expects to ship about 55 EUV systems this year, it said.
“We were able to put the fire out in a couple of hours, but still there was significant damage,” ASML chief executive officer Peter Wennink said in a statement. “Because of the hard work and the creativity, we currently believe that we can manage the situation and that we will not see a significant impact on our EUV output in the year 2022.” 
Wennink said demand is 40 to 50 percent above the ASML’s maximum capacity, and it would take “two to three years to get a nice balance between supply and demand.” 
The firm’s shipments would increase next year, he added.
Additional reporting by Bloomberg

                                                                                Global smartphone shipments are expected to fall 3.5 percent to 1.31 billion units this year, market research firm International Data Corp (IDC) said in a report yesterday, as it reversed downward its previous forecast of an annual 1.6 percent increase.
IDC attributed the downward projection to three consecutive quarters of decline in shipments, and increasing supply and demand challenges, the report said.
However, the market researcher expects the decline to be a “short-term setback” and retained its five-year compound annual growth rate projection of 1.9 percent through 2026, as it expects the market to rebound next year, it said.
“The smartphone industry is                                    
LIMITED EFFECT:
                                        The impact on supply chains is easing in Shanghai, chairman Young Liu said, adding that Hon Hai is confident that supply chains are stabilizing                                        Hon Hai Precision Industry Co (鴻海精密), a key iPhone assembler, yesterday said supply chain turbulence in China would improve in the second half of this year as Shanghai lifts COVID-19 restrictions at an orderly pace.
The company, based in New Taipei City’s Tucheng District (土城), said “logistics posed a great challenge,” although most of its more than 30 manufacturing campuses in China have not been affected by Beijing’s strict “zero COVID-19” policy and a two-month lockdown in Shanghai.
Hon Hai said it has stepped up efforts to arrange workers’ accommodations to maintain normal production under the so-called “closed loop” model. 
The company                                    

                                                                                Tourism firms are planning to recruit new workers in the hope that the government would ease or lift border restrictions in the second half of this year.
Taiwan has had one of the world’s strictest border controls during the COVID-19 pandemic including a ban on foreign tourists. The nation also required all overseas arrivals to undergo 14 days of quarantine from March 2020 to March this year.
The restrictions have led to a considerable decline in overseas arrivals, from 11.86 million in 2019 to 140,479 last year, hurting companies catering to international travelers.
The mandatory quarantine period was in March lowered to 10                                    

                                                                                MediaTek Inc (聯發科), the world’s biggest mobile phone chip supplier, yesterday said it is upbeat about market demand in the long term, driven by accelerating digital transformation worldwide.
The company’s comments came in response to shareholders’ concern about chip demand after smartphones and PC sales weakened over the past six months.
The outbreak of the COVID-19 pandemic stimulated massive demand for computers, communications and consumer electronics, as people worked remotely and learned from home, MediaTek chairman Tsai Ming-kai (蔡明介) said.
“Over the past half year, demand has reduced, as some demand has been satisfied, or because countries in Europe and the US have                                    
    """
    timestamp = '1'
    res = cworker.company_count(text, timestamp)
    assert(len(res) == 2)
    assert(res[0].get('Word_Count') == 4)
    assert(res[1].get('Word_Count') == 7)
