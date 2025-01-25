import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
from keras import regularizers
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def train_model(feature_csv_path, merged_data_csv_path):
    # Importing the dataset
    df = pd.read_csv(feature_csv_path)

    # Preprocessing the dataset for LSTM
    features = df.drop(['Date', 'Close'], axis=1).values
    target = df['Close'].values

    scalerFeatures = MinMaxScaler(feature_range=(0, 1))
    scalerTarget = MinMaxScaler(feature_range=(0, 1))

    featuresScaled = scalerFeatures.fit_transform(features)
    targetScaled = scalerTarget.fit_transform(target.reshape(-1, 1))

    lookBack = 3
    X, y = createDataset(featuresScaled, targetScaled, lookBack)
    print(X[:2])
    print(y[:2])

    trainSize = int(len(X) * 0.8)
    testSize = len(X) - trainSize
    trainX, testX = X[0:trainSize, :], X[trainSize:len(X), :]
    trainY, testY = y[0:trainSize], y[trainSize:len(y)]

    trainX = np.reshape(trainX, (trainX.shape[0], lookBack, trainX.shape[2]))
    testX = np.reshape(testX, (testX.shape[0], lookBack, testX.shape[2]))

    # Building the LSTM model
    batchSize = 1
    epoch = 20
    neurons = 100
    dropout = 0.6

    model = Sequential()
    model.add(LSTM(neurons, return_sequences=True, activation='tanh', input_shape=(lookBack, features.shape[1])))
    model.add(Dropout(dropout))
    model.add(LSTM(neurons, return_sequences=True, activation='tanh'))
    model.add(Dropout(dropout))
    model.add(LSTM(neurons, activation='tanh'))
    model.add(Dropout(dropout))

    model.add(Dense(units=1, activation='linear', activity_regularizer=regularizers.l1(0.00001)))
    model.add(Activation('tanh'))
    model.summary()

    model.compile(loss='mean_squared_error', optimizer='RMSprop')

    model.fit(trainX, trainY, epochs=epoch, batch_size=batchSize, verbose=1, validation_split=0.2)

    # Testing the model
    # Running prediction over the training set and testing set
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    trainPredictInv = scalerTarget.inverse_transform(trainPredict)
    trainYInv = scalerTarget.inverse_transform(np.reshape(trainY, (trainY.shape[0], 1)))
    testPredictInv = scalerTarget.inverse_transform(testPredict)
    testYInv = scalerTarget.inverse_transform(np.reshape(testY, (testY.shape[0], 1)))

    # Calculating the score and accuracy of the model
    trainScore = np.sqrt(mean_squared_error(trainYInv[:, 0], trainPredictInv[:, 0]))
    print(f'Training RMSE: {trainScore}')
    testScore = np.sqrt(mean_squared_error(testYInv[:, 0], testPredictInv[:, 0]))
    print(f'Testing RMSE: {testScore}')

    trainAccuracy = 100 - (trainScore / np.mean(trainYInv) * 100)
    testAccuracy = 100 - (testScore / np.mean(testYInv) * 100)

    print(f'Training Accuracy: {trainAccuracy:.2f}%')
    print(f'Testing Accuracy: {testAccuracy:.2f}%')

    # Visualizing the data
    dates = df['Date'].values
    sampleInterval = 60
    sampledDates = dates[::sampleInterval]

    plt.figure(figsize=(20, 10))
    plt.plot(dates[:len(trainY)], trainY, label='Actual Train')
    plt.plot(dates[:len(trainPredict)], trainPredict, label='Predicted Train')
    plt.plot(dates[len(trainY):len(trainY) + len(testY)], testY, label='Actual Test')
    plt.plot(dates[len(trainPredict):len(trainPredict) + len(testPredict)], testPredict, label='Predicted Test')

    plt.xticks(sampledDates, rotation=90)

    plt.legend()
    plt.show() 

# Creating a function to preprocess the dataset
def createDataset(dataset, target, lookBack=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - lookBack):
        a = dataset[i:(i + lookBack), :]
        dataX.append(a)
        dataY.append(target[i + lookBack])
    return np.array(dataX), np.array(dataY)

