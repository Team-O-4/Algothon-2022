import numpy as np
import pandas as pd
from typing import Optional


prevPos: Optional[np.array] = None


def getMyPosition(histPrice: np.array):
    global prevPos
    nInst: int
    nDays: int
    nInst, nDays = histPrice.shape

    posDelta: np.array = np.zeros(nInst)
    priceEwm12: np.array = (pd
                          .DataFrame(histPrice)
                          .ewm(span=12, axis=1)
                          .mean()
                          .to_numpy())
    priceEwm26: np.array = (pd
                          .DataFrame(histPrice)
                          .ewm(span=26, axis=1)
                          .mean()
                          .to_numpy())
    priceMACD: np.array = priceEwm12 - priceEwm26
    priceIndicator: np.array = priceMACD > 0

    # if nDays == 249:
    #     posDelta[:] = -prevPos
    if nDays > 2:
        posDelta = (priceIndicator[:, -2] != priceIndicator[:, -1]) \
                * (priceIndicator[:, -1] - .5) * 10

    if prevPos is None:
        prevPos = np.zeros(nInst)
    pos = prevPos + posDelta
    prevPos = pos
    return prevPos

