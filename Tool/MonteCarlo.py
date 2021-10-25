import numpy as np
#import matplotlib.pyplot as plt


def simulation_path(P0, r, v, dt, N):
    Pt = np.log(P0) + np.cumsum(((r - ((v**2)/2))*dt +
                                                     v*np.sqrt(dt) * np.random.normal(size=(n, N))), axis=0)
    Pt = np.round_(Pt, decimals=2)
    return np.exp(Pt) 







# inputs
P0 = 100             # initial stock price
K = 110              # strike
r = 0.05             # annual interest rate
v = 0.25             # volatility
dt = 30/365          # timeperiod
N = 60000            # number of simulations
n =  3               # number of steps
TTM = 90/365         # time to maturity
OptionType = "Lookback"      
CallPut = "Call"

paths = simulation_path(P0, r, v, dt, N)

if OptionType == "EU":
    if CallPut == "Call":
           payoffs = np.maximum(paths[-1]-K, 0)
    elif CallPut == "Put":
           payoffs = np.maximum(K-paths[-1], 0)
elif OptionType == "US":
    if CallPut == "Call":
       None     
    elif CallPut == "Put":
       None      
elif OptionType == "Asian":
    if CallPut == "Call":
       None    
    elif CallPut == "Put":
       None      
elif OptionType == "Bermudan":
    if CallPut == "Call":
       None
    elif CallPut == "Put":
       None
elif OptionType == "Chooser":
       None
elif OptionType == "LookBack":
    if CallPut == "Call":
       max_=np.max(paths,axis=0)
       payoffs = np.maximum(max_-K, 0)
    elif CallPut == "Put":
       min_=np.min(paths,axis=0)
       payoffs = np.maximum(K-min_, 0)
elif OptionType == "Barrier":
    pass


option_price = np.mean(payoffs)*np.exp(-r*TTM) # discounting back to present value
print(option_price)






# plt.plot(paths)
# plt.xlabel("Time Increments")
# plt.ylabel("Stock Price")
# plt.title("Geometric Brownian Motion")
