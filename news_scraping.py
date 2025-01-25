from requests_html import HTMLSession, PyQuery as pq
from datetime import datetime, timedelta
import json
import numpy as np


# function to scrape news accepting a start date, website url, output file path, and scraping rate limit
def scrape_news(start_date, website_url, output_file_path, scraping_rate_limit):
    session = HTMLSession()

    # Selecting the date range for news
    startDate = start_date
    endDate = datetime.now().date()
    dt = timedelta(days=1)

    # Scrape the news headings from the source website
    f = open(output_file_path, 'w', encoding='utf-8')
    allData = {}

    for i in np.arange(startDate, endDate, dt).astype(datetime):
        while 1:
            temp = f'{website_url}/{str(i.date())}'
            print(temp)
            r = session.get(temp)
            articles = r.html.find('article')
            
            if len(articles) > 0:
                break
        
            print("in while")
        
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
    json.dump(allData, f, ensure_ascii=False)
    f.close() 