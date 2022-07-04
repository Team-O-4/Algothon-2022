import numpy as np
import pandas as pd
import time
from teamName import getMyPosition as getPosition

nInst = 0
nt = 0

# Commission rate
commRate = 0.0025 # was 0.0050

# Dollar position limit (maximum absolute dollar value of any individual stock position)
dlrPosLimit = 10000

timeOut=600 

def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices.txt"
prcAll = loadPrices(pricesFile)
print ("Loaded %d instruments for %d days" % (nInst, nt))

#currentPos = np.zeros(nInst)

def calcPL(prcHist):
    global tStart
    cash = 0
    curPos = np.zeros(nInst)
    totDVolume = 0
    frac0 = 0.
    frac1 = 0.
    value = 0
    todayPLL = []
    (_,nt) = prcHist.shape
    tNow = time.time()
    for t in range(1,nt+1): 
        prcHistSoFar = prcHist[:,:t]
        # no trades on the very last price update, only before the last update
        newPosOrig = curPos
        tNow = time.time()
        tRunning = tNow - tStart
        #print ("tRunning: %.4lf" % tRunning)
        if (t < nt) and (tRunning <= timeOut):
            newPosOrig = getPosition(prcHistSoFar)
            # otherwise keep the same desired positions
        if (tRunning > timeOut):
            print ("TIME OUT [ %.3lf > %lf]!" % (tRunning, timeOut))
        curPrices = prcHistSoFar[:,-1] #prcHist[:,t-1]
        posLimits = np.array([int(x) for x in dlrPosLimit / curPrices])
        newPos = np.array([int(p) for p in np.clip(newPosOrig, -posLimits, posLimits)])
        deltaPos = newPos - curPos
        dvolumes = curPrices * np.abs(deltaPos)
        dvolume = np.sum(dvolumes)
        totDVolume += dvolume
        comm = dvolume * commRate
        cash -= curPrices.dot(deltaPos) + comm
        curPos = np.array(newPos)
        posValue = curPos.dot(curPrices)
        todayPL = cash + posValue - value
        todayPLL.append(todayPL)
        value = cash + posValue
        ret = 0.0
        if (totDVolume > 0):
            ret = value / totDVolume
        print ("Day %d value: %.2lf todayPL: $%.2lf $-traded: %.0lf return: %.5lf" % (t,value, todayPL, totDVolume, ret))
    pll = np.array(todayPLL)
    (plmu,plstd) = (np.mean(pll), np.std(pll))
    annSharpe = 0.0
    if (plstd > 0):
        annSharpe = 16 * plmu / plstd
    return (plmu, ret, annSharpe, totDVolume)



tStart = time.time()
(meanpl, ret, sharpe, dvol) = calcPL(prcAll)
tEnd = time.time()
tRun = tEnd - tStart
print ("=====")
print ("mean(PL): %.0lf" % meanpl)
print ("return: %.5lf" % ret)
print ("annSharpe(PL): %.2lf " % sharpe)
print ("totDvolume: %.0lf " % dvol)
print ("runTime  : %.3lf " % tRun)




