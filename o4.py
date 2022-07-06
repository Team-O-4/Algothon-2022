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
    priceEwm: np.array = (pd
                          .DataFrame(histPrice)
                          .ewm(span=5, axis=1)
                          .mean()
                          .to_numpy())

    if nDays > 1:
        posDelta = histPrice[:, -1] - priceEwm[:, -1] * 100

    if prevPos is None:
        prevPos = np.zeros(nInst)
    pos = prevPos + posDelta
    prevPos = pos
    return prevPos

