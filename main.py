from datetime import datetime
from news_scraping import scrape_news
from data_prep import prepare_data
from training import train_model
from sentiment_analysis import analyze_sentiment

website_url = 'https://www.dawn.com/archive/latest-news/'
start_date = datetime(2024, 1, 1)
end_date = datetime.now().date()
scraping_rate_limit = 1000
data_prep_csv_path = './data/stocks/hbl_feat.csv'
daily_scores_json_path = './data/news/daily_scores.json'
merged_data_csv_path = './data/stocks/hbl_merged.csv'
sentimentInputJsonFile = './data/news/headlines.json'
sentimentOutputJsonFile = './data/news/daily_scores.json'
feature_csv_path = './data/stocks/hbl_feat.csv'

scrape_news(start_date, website_url, './data/news/headlines.json', scraping_rate_limit)

prepare_data(data_prep_csv_path, daily_scores_json_path, merged_data_csv_path)

train_model(feature_csv_path, merged_data_csv_path)

analyze_sentiment(sentimentInputJsonFile, sentimentOutputJsonFile)

