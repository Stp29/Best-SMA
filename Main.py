import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

daysToHoldStock = 14
name = 'DVAX'

ticker = yfinance.Ticker(name)
data = ticker.history(period="max", interval="1d")
data['Forward Close'] = data['Close'].shift(-daysToHoldStock)
data['Forward Return'] = (data['Forward Close'] - data['Close'])/data['Close']

result = []
train_size = 0.6
for sma_length in range(20, 500):
    data['SMA'] = data['Close'].rolling(sma_length).mean()
    data['input'] = [int(x) for x in data['Close'] > data['SMA']]

    df = data.dropna()
    training = df.head(int(train_size * df.shape[0]))
    test = df.tail(int((1 - train_size) * df.shape[0]))

    tr_returns = training[training['input'] == 1]['Forward Return']
    test_returns = test[test['input'] == 1]['Forward Return']
    mean_forward_return_training = tr_returns.mean()
    mean_forward_return_test = test_returns.mean()
    pvalue = ttest_ind(tr_returns, test_returns, equal_var=False)[1]

    result.append({
        'sma_length': sma_length,
        'training_forward_return': mean_forward_return_training,
        'test_forward_return': mean_forward_return_test,
        'p-value': pvalue
    })

result.sort(key = lambda x : -x['training_forward_return'])

print(result[0])