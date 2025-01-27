from datetime import datetime, timedelta
import json
import time
from bs4 import BeautifulSoup
import requests

def scrape_news(website_url, sentimentInputJsonFile, stock_symbol):
    # Initialize the date range for news
    end_date = datetime.now().date()
    keywords = stock_symbol[1]
    allData = {}

    print(f"Fetching: {website_url}")
    
    # scrape news
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        heading = article.find('h2').text.strip()
        print(heading)
        
    # Write the collected data to the output file
    # with open(sentimentInputJsonFile, 'w', encoding='utf-8') as f:
    #     json.dump(allData, f, ensure_ascii=False)

