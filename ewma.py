import numpy as np
import pandas as pd
from typing import Optional
from sklearn.preprocessing import MinMaxScaler


prevPos: Optional[np.array] = None


def getMyPosition(histPrice: np.array):
    global prevPos
    nInst: int
    nDays: int
    nInst, nDays = histPrice.shape

    posDelta: np.array = np.zeros(nInst)
    # histPrice = np.log(histPrice)
    priceEwm: np.array = (pd
                            .DataFrame(histPrice)
                            .ewm(span=5, axis=1)
                            .mean()
                            .to_numpy())

    if nDays > 1:
        x = np.arange(nDays)
        b1_short = np.corrcoef(x, histPrice)[0][1] *(np.std(histPrice) / np.std(x))
        b0_short = np.mean(histPrice) - b1_short * np.mean(x)

        if b1_short > 0.9:
            posDelta = 100
        else:
            posDelta = -100000000

    if prevPos is None:
        prevPos = np.zeros(nInst)
    pos = prevPos + posDelta
    prevPos = pos
    return prevPos