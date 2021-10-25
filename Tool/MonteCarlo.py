import numpy as numpy
import matplotlib.pyplot as plt

def simulation_path(PStock, interest, volatilty, periodLength, N):
       PstockFuture = numpy.log(PStock) + numpy.cumsum(((r - sigma**2/2)*periodLength) + volatilty*numpy.sqrt(periodLength) * numpy.random.normal(size=(steps,N))),axis=0)
       PstockFuture = round(PstockFuture, decimals = 2)
       return PstockFuture

#inputs
PStock = 50
interest - 0.1
volatilty = 0.4
periodLength = 30/365
N = 100
maturity = 90/365

steps = maturity/periodLength

paths = simulation_path(PStock, interest, volatilty, periodLength, N)

plt.plot(paths);
plt.xlabel("Time Increments")
plt.ylabel("Stock Price")
plt.title("Geometric Brownian Motion")
