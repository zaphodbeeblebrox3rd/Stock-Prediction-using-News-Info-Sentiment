import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json


# Writing functions to calculate average sentiment for each day
def calculateDailySentiment(headlines):
    texts = [headline['heading'] for headline in headlines]
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512, return_attention_mask=True)
    outputs = model(**inputs)
    logits = outputs.logits
    scores = logits.softmax(dim=1)
    averageScore = scores.mean(dim=0).tolist()
    return averageScore

def analyzeAndSaveSentiment(inputFile, outputFile):
    with open(inputFile, 'r') as file:
        data = json.load(file)

    result = {}

    for date, headlines in data.items():
        averageScore = calculateDailySentiment(headlines)
        print(f"{date} > {averageScore}")
        result[date] = averageScore

    with open(outputFile, 'w') as outputFile:
        json.dump(result, outputFile, indent=2)

def analyze_sentiment(sentimentInputJsonFile, sentimentOutputJsonFile):
    # Importing a sentiment model from Huggingface
    modelName = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    model = AutoModelForSequenceClassification.from_pretrained(modelName)

    analyzeAndSaveSentiment(sentimentInputJsonFile, sentimentOutputJsonFile)