import numpy as np
from typing import Optional


prevPos: Optional[np.array] = None


def getMyPosition(histPrice: np.array):
    global prevPos
    nInst: int
    nDays: int
    nInst, nDays = histPrice.shape

    posDelta: np.array = np.zeros(nInst)

    if nDays > 1:
        posDelta = np.sign(histPrice[:, -1] - histPrice[:, -2]) * 100_000_000

    if prevPos is None:
        prevPos = np.zeros(nInst)
    pos = prevPos + posDelta
    prevPos = pos
    return prevPos

