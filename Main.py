import yfinance
import pandas as pd
import numpy as np
import math
from scipy.stats import ttest_ind

name = 'DVAX'
startDate = '2020-01-01'
endDate = '2021-03-26'

printResult = []
for daysToHoldStock in range(1,200):

    ticker = yfinance.Ticker(name)
    data = ticker.history(interval="1d", start=startDate, end=endDate)
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

        if math.isnan(pvalue) == False and pvalue > 0.05:
            result.append({
                'days-to-hold': daysToHoldStock,
                'sma_length': sma_length,
                'training_forward_return': mean_forward_return_training,
                'test_forward_return': mean_forward_return_test,
                'p-value': pvalue
            })

    result.sort(key = lambda x : -x['training_forward_return'])

    if len(result) >= 1:
        printResult.append(result[0])

for p in printResult:
    print(p)