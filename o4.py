from cgi import test
import numpy as np
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

prevPos: Optional[np.array] = None





def getMyPosition(histPrice: np.array):
    global prevPos
    nInst: int
    nDays: int
    nInst, nDays = histPrice.shape

    posDelta: np.array = np.zeros(nInst)

    # scale to 0 to 1
    for i in range(nInst):
        histPrice[i] /= np.max(histPrice[i])

    # select a random half of the instruments to be training data
    # np.random.seed(69)

    # training_size = int(nInst/2)
    # idx = np.random.choice(histPrice.shape[0], training_size, replace=False)

    # training_data = histPrice[idx, :]

    inst_1 = histPrice[0]

    train_x = []
    train_y = []

    len_validate = 50
    len_train = 60

    # train the model with the first 200 days
    for i in range(len_train, len(inst_1)-len_validate):
        train_x.append(inst_1[i-len_train: i])
        train_y.append(inst_1[i])

    train_x = np.array(train_x)
    train_y = np.array(train_y)
   
    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))

    lstm_model = Sequential()
    lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(train_x.shape[1], 1)))
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss='mean_squared_error', optimizer='adadelta')
    lstm_model.fit(train_x, train_y, epochs=3, batch_size=1, verbose=2)

    # predict future stock prices
    past_price = inst_1[len(inst_1) - (len_validate) - 1 - len_train:]
    past_price = past_price.reshape(-1, 1)

    test_result = []

    for i in range(len_train, past_price.shape[0]):
        test_result.append(past_price[i-60:i, 0])

    test_result = np.array(test_result)
    test_result.reshape(test_result, (test_result.shape[0], test_result.shape[1],1))

    model_prediction = lstm_model.predict(test_result)
    print(model_prediction)


    if nDays > 1:
        posDelta = np.sign(histPrice[:, -1] - histPrice[:, -2]) * 100_000_000

    if prevPos is None:
        prevPos = np.zeros(nInst)
    pos = prevPos + posDelta
    prevPos = pos
    return prevPos

