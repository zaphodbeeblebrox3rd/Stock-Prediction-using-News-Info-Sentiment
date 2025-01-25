from requests_html import HTMLSession, PyQuery as pq
from datetime import datetime, timedelta
import json
import numpy as np

session = HTMLSession()

# Selecting the date range for news
startDate = datetime(2015, 1, 1)
endDate = datetime.now().date()
dt = timedelta(days=1)

# Scrape the news headings from the source website
# Website source used: DAWN News
f = open('./data/news2023/headlines.json', 'w', encoding='utf-8')
allData = {}

for i in np.arange(startDate, endDate, dt).astype(datetime):
    while 1:
        temp = f'https://www.dawn.com/archive/latest-news/{str(i.date())}'
        print(temp)
        r = session.get(temp)
        articles = r.html.find('article')
        
        if len(articles) > 0:
            break
        #endif
        
        print("in while")
    #endwhile
        
    print(f"{str(i.date())} > {len(articles)} articles fetched")
    allData[str(i.date())] = []
    
    for article in articles:
        t = pq(article.html)
        headingText = t('h2.story__title a.story__link').text()
        spanId = t('span').eq(0).attr('id')
        label = spanId.lower() if spanId is not None else None
        
        if len(headingText) > 0 and label in ["business", "pakistan"]:
            allData[str(i.date())].append({
                "heading": headingText,
                "label": label,
            })
        #endif
    #endfor
#endfor
    
json.dump(allData, f, ensure_ascii=False)
f.close() 