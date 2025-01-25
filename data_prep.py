import pandas as pd
import json
import matplotlib.pyplot as plt

def prepare_data(data_prep_csv_path, daily_scores_json_path, merged_data_csv_path):
    # Importing daily scores from news folder
    with open(daily_scores_json_path, 'r') as file:
        sentimentScores = json.load(file)

    dfSentiment = pd.DataFrame(list(sentimentScores.items()), columns=['jsonDate', 'sentiment'])
    dfSentiment['date'] = pd.to_datetime(dfSentiment['jsonDate'], format='%Y-%m-%d')
    dfSentiment.head()

    # Importing daily stock data from stock folder
    dfCsv = pd.read_csv(data_prep_csv_path)
    dfCsv.head()

    # Merge both the imported data with date
    dfCsv['date'] = pd.to_datetime(dfCsv['Date'], format='%d-%b-%Y')
    dfMerged = pd.merge(dfCsv, dfSentiment, on='date', how='left')
    dfSentimentColumns = pd.DataFrame(dfMerged['sentiment'].tolist(), columns=['feature1', 'feature2', 'feature3', 'feature4', 'feature5'])
    dfMerged = pd.concat([dfMerged, dfSentimentColumns], axis=1)

    dfMerged = dfMerged.drop(columns=['Symbol', 'date', 'sentiment', 'jsonDate'])
    dfMerged.head()

    # Saving the merged data
    # Saving the file in CSV format
    dfMerged.to_csv(merged_data_csv_path, index=False)

    # Check data by plotting the graph
    dfMerged[['Close']].plot()
    plt.title('Stock Close Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.show() 