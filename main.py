from datetime import datetime
from news_scraping import scrape_news
from data_prep import prepare_data
from training import train_model
from sentiment_analysis import analyze_sentiment
import yfinance as yf


# websites as a list
website_url = ['https://crawl4ai.com', 'https://www.theguardian.com/world/us-news']
start_date = datetime(2024, 1, 1)
end_date = datetime.now().date()
scraping_rate_limit = 0.25

# List of stock symbols with associated keywords
stock_symbols = [
    ("NVDA", ["gpu", "ai", "nVidia"]),
    ("META", ["social media", "META", "Facebook"]),
    ("TSMC34.SA", ["semiconductor", "chip", "manufacturing"]),
    ("GOOG", ["search", "Alphabet", "Google"]),
    ("TSLA", ["EV", "Tesla"]),
    ("CIFR", ["mining", "blockchain", "Cipher Mining"]),
    ("UNFI", ["United Natural Foods", "organic"]),
    ("PBPB", ["Potbelly", "sandwich", "food"]),
    ("SAVEQ", ["airline", "Spirit"])
]

for stock_symbol in stock_symbols:
    print(f"Processing stock: {stock_symbol[0]}")

    # Define file paths specific to each stock symbol
    data_prep_csv_path = f'./data/stocks/{stock_symbol[0]}_feat.csv'
    daily_scores_json_path = f'./data/news/{stock_symbol[0]}_daily_scores.json'
    merged_data_csv_path = f'./data/stocks/{stock_symbol[0]}_merged.csv'
    sentimentInputJsonFile = f'./data/news/{stock_symbol[0]}_headlines.json'
    sentimentOutputJsonFile = f'./data/news/{stock_symbol[0]}_daily_scores.json'
    feature_csv_path = f'./data/stocks/{stock_symbol[0]}_feat.csv'
    
    # scrape news
    for website in website_url:
        try:
            scrape_news(website, sentimentInputJsonFile, stock_symbol))
        except Exception as e:
            print(f"Error scraping news: {e}")

    # get stock data
    try:
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error getting stock data: {e}")

    # prepare data
    try:
        prepare_data(data_prep_csv_path, daily_scores_json_path, merged_data_csv_path)
    except Exception as e:
        print(f"Error preparing data: {e}")

    # analyze sentiment
    try:
        analyze_sentiment(sentimentInputJsonFile, sentimentOutputJsonFile)
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")

    # train model
    try:
        train_model(feature_csv_path, merged_data_csv_path)
    except Exception as e:
        print(f"Error training model: {e}")


