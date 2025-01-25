from datetime import datetime
from news_scraping import scrape_news
from data_prep import prepare_data
from training import train_model
from sentiment_analysis import analyze_sentiment

# websites as a list
website_url = ['https://crawl4ai.com', 'https://www.theguardian.com/world/us-news']

start_date = datetime(2024, 1, 1)
end_date = datetime.now().date()
scraping_rate_limit = 0.25
data_prep_csv_path = './data/stocks/hbl_feat.csv'
daily_scores_json_path = './data/news/daily_scores.json'
merged_data_csv_path = './data/stocks/hbl_merged.csv'
sentimentInputJsonFile = './data/news/headlines.json'
sentimentOutputJsonFile = './data/news/daily_scores.json'
feature_csv_path = './data/stocks/hbl_feat.csv'
keywords = [
    "business",
    "energy",
    "trump",
    "senate",
    "house",
    "supreme",
    "court",
    "surge",
    "law",
    "offshoring",
    "tech",
    "stock",
    "conflict",
    "attack",
    "war",
    "ai",
    "gpu",
    "llm",
    "model"
]

scrape_news(start_date, website_url, sentimentInputJsonFile, scraping_rate_limit, keywords)

prepare_data(data_prep_csv_path, daily_scores_json_path, merged_data_csv_path)

train_model(feature_csv_path, merged_data_csv_path)

analyze_sentiment(sentimentInputJsonFile, sentimentOutputJsonFile)

