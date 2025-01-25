import pandas as pd
import json
import matplotlib.pyplot as plt

# Importing daily scores from news folder
with open('./data/news2023/daily_scores.json', 'r') as file:
    sentimentScores = json.load(file)
#endwith

dfSentiment = pd.DataFrame(list(sentimentScores.items()), columns=['jsonDate', 'sentiment'])
dfSentiment['date'] = pd.to_datetime(dfSentiment['jsonDate'], format='%Y-%m-%d')
dfSentiment.head()

# Importing daily stock data from stock folder
# Data used will be of Habib Bank Limited (HBL)
csvFilePath = './data/stocks2023/hbl.csv'
dfCsv = pd.read_csv(csvFilePath)
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
outputCsvPath = './data/stocks2023/hbl_feat.csv'
dfMerged.to_csv(outputCsvPath, index=False)

# Check data by plotting the graph
dfMerged[['Close']].plot()
plt.show() 