

# Create your views here.
import matplotlib
from django.shortcuts import render
import requests
import datetime as dt
import pandas as pd
import numpy as np
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.preprocessing.sequence import TimeseriesGenerator
import yfinance as yf
import matplotlib.pyplot as plt

def index(request):
    return render(request, 'myapp/index.html')


def CryptoRate(request):
    # API key to access the rates
    ApiKey = 'd77eb42187b3622a83f1bba9fb267e6053dfa18f25c1c652a2cba6a3e107b5d0'

    # CryptoCompare API URL
    CurrentRates_url = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD&api_key={ApiKey}'

    # To get current rates of crypto through API
    try:
        response = requests.get(CurrentRates_url)
        data = response.json()
        BitcoinPrice = data.get('BTC', {}).get('USD')
        EthereumPrice = data.get('ETH', {}).get('USD')
    except Exception as e:
        BitcoinPrice = None
        EthereumPrice = None

    #To display the values to the template
    return render(request, 'myapp/crypto_rate.html', {
        'BitcoinPrice': BitcoinPrice,
        'EthereumPrice': EthereumPrice,
    })



def BitcoinPrediction(request):

    # Getting the data
    symbol = 'BTC-USD'
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime.now()
    df = yf.download(symbol, start=start_date, end=end_date)

    #Considering the close column
    Data = df["Close"]
    Data = pd.DataFrame(Data)
    print(type(Data))
    Data.head(5)

    #Preprocessing the data
    scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaledData = scaler.fit_transform(Data)

    len(df)

     #Splitting the data
    train = scaledData[:2700]
    validation = scaledData[2700:2900]
    test = scaledData[2900:]

    print(train.shape)
    print(validation.shape)
    print(test.shape)

    #Time Series Generator
    trainGen = TimeseriesGenerator(data=train, targets=train, length=2,
                                   sampling_rate=1, stride=1,
                                   shuffle=False, reverse=False,
                                   batch_size=8)
    valGen = TimeseriesGenerator(data=validation, targets=validation, length=2,
                                 sampling_rate=1, stride=1,
                                 shuffle=False, reverse=False,
                                 batch_size=8)
    testGen = TimeseriesGenerator(data=test, targets=test, length=2,
                                  sampling_rate=1, stride=1,
                                  shuffle=False, reverse=False,
                                  batch_size=8)

    #Applying the model
    BTC = Sequential()
    BTC.add(LSTM(32, return_sequences=False, input_shape=(2, 1)))
    BTC.add(Dense(1))
    print(BTC.summary())

    #Compiling the model
    BTC.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae', 'mse'])
    history = BTC.fit_generator(trainGen, validation_data=valGen,
                                epochs=50, verbose=1)

    #Plot the graph to see the epoch loss
    import matplotlib.pyplot as plt
    matplotlib
    inline
    plt.figure(figsize=[9, 7])
    plt.plot(history.history['loss'], 'r', linewidth=3.0)
    plt.legend(['Training loss', 'Validation Loss'], fontsize=18)
    plt.xlabel('Epochs ', fontsize=16)
    plt.ylabel('Loss', fontsize=16)
    plt.title('Loss Curves', fontsize=16)
    plt.grid(True)

    # Generate predictions
    predictions = BTC.predict_generator(testGen)
    predictions = scaler.inverse_transform(predictions)
    test = scaler.inverse_transform(test)

    #Fetch the present date
    PresentRate = df["Close"].iloc[-1]
    print(PresentRate)

    #Print the predicted rate
    PredictedRated = predictions[-1][0]
    print(PredictedRated)

     #Recommendation based on the predicted rate
     if PredictedRated> PresentRate:
         recommendation = ("It is recommended to buy crypto.")
     elif PredictedRated<PresentRate:
         recommendation = ("It is not recommended to buy crypto. It is recommended to sell your crypto")
     else:
         recommendation = ("The predicted rate is similar to the present rate. Consider holding your crypto")

    plt.figure(figsize=[7, 5])
    plt.plot(predictions, '--', label='Predictions')
    plt.plot(test, label='Actual')
    plt.xlabel("Observation")
    plt.ylabel("Price")
    plt.title("BTC Rate Prediction Vs. Actual")
    plt.legend()
    plt.grid(True)
    plt.show()

    context = {
        'predictions': predictions,
        'test_data': test
        'recommendation': recommendation
    }
    return render(request, 'myapp/Prediction_rate.html', context)










