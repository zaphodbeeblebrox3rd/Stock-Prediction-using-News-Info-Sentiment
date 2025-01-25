import asyncio
from crawl4ai import *
from datetime import datetime, timedelta
import json
import time

async def scrape_news(start_date, website_url, sentimentInputJsonFile, scraping_rate_limit, keywords):
    # Initialize the date range for news
    end_date = datetime.now().date()
    dt = timedelta(days=1)

    allData = {}

    for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
        date_str = single_date.strftime("%Y-%m-%d")
        url = f'{website_url}/{date_str}'
        print(f"Fetching: {url}")

        try:
            page = await scrape_news_async(url, scraping_rate_limit, keywords)
            articles = page.select('article')

            print(f"{date_str} > {len(articles)} articles fetched")
            allData[date_str] = []

            # for article in articles:
            #     heading_tag = article.select_one('h2.story__title a.story__link')
            #     heading_text = heading_tag.get_text(strip=True) if heading_tag else ''
            #     span_tag = article.select_one('span')
            #     label = span_tag['id'].lower() if span_tag and 'id' in span_tag.attrs else None

            #     if heading_text and (label in keywords or any(keyword in heading_text.lower() for keyword in keywords)):
            #         allData[date_str].append({
            #             "heading": heading_text,
            #             "label": label,
            #         })

        except Exception as e:
            print(f"Error fetching {website_url}: {e}")


    # Write the collected data to the output file
    # with open(sentimentInputJsonFile, 'w', encoding='utf-8') as f:
    #     json.dump(allData, f, ensure_ascii=False)

async def scrape_news_async(website_url, scraping_rate_limit, keywords):
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=website_url)

        # Print the extracted content
        print(result.markdown)



# Example usage:
# scrape_news(datetime(2015, 1, 1), 'https://www.dawn.com/archive/latest-news', './data/news2023/headlines.json') 