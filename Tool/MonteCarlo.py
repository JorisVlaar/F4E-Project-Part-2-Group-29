import numpy as np
import array
import matplotlib.pyplot as plt

# Standard inputs
P0 = 100             # initial stock price
K = 110              # strike
r = 0.05             # annual interest rate
v = 0.25             # volatility
TTM = 1              # time to maturity
Barrier = 105        # Barrier
N = 60000  # number of simulations
n = 270 # number of steps
OptionType = "BARRIER"
CallPut = "CALL"
InOut = "IN"
UpDown = "UP"

# P0 = int(input("Enter initial stock price: "))
# K = int(input("Enter strike price: "))
# r = float(input("Enter the annual interest rate as a fraction: "))
# v = float(input("Enter the volatility as a fraction: "))
# TTM = float(input("Enter the Time to Maturity in years: "))
# Barrier = int(input("Enter the Barrier level: "))
# OptionType = input("Enter the option type (choose from EU,US,ASIAN,BERMUDAN,CHOOSER, LOOKBACK, BARRIER): ").upper()
# if "BARRIER" in OptionType:
#     InOut = input("Enter the barrier type (choose from IN, OUT): ").upper()
#     UpDown = input("Enter the barrier type (choose from UP, DOWN): ").upper()
# CallPut = input("Choose between: CALL, PUT ").upper()


def simulation_path(P0, r, v, n, N, TTM):
    dt = TTM / n
    Pt = np.log(P0) + np.cumsum(((r - ((v ** 2) / 2)) * dt +
                                 v * np.sqrt(dt) * np.random.normal(size=(n, N))), axis=0)
    Pt = np.round_(Pt, decimals=2)
    return np.exp(Pt)


def monteCarloTool():
    paths = simulation_path(P0, r, v, n, N, TTM)
    if "EU" in OptionType:
        if "CALL" in CallPut:
            payoffs = np.maximum(paths[-1] - K, 0)
        elif "PUT" in CallPut:
            payoffs = np.maximum(K - paths[-1], 0)
    elif "US" in OptionType:
        if "CALL" in CallPut:
            None
        elif "PUT" in CallPut:
            None
    elif "ASIAN" in OptionType:
        avg_ = np.average(paths, axis=0)
        #     if CallPut == "Call":
        #         payoffs = np.max(avg_-K, 0)
        #     elif CallPut == "Put":
        #         payoffs = np.max(K-avg_, 0)
        if "CALL" in CallPut:
            payoffs = np.maximum(paths[-1] - avg_, 0)
        elif "PUT" in CallPut:
            payoffs = np.maximum(avg_ - paths[-1], 0)

    elif "BERMUDAN" in OptionType:
        if "CALL" in CallPut:
            None
        elif "PUT" in CallPut:
            None
    elif "CHOOSER" in OptionType:
        None
    elif "LOOKBACK" in OptionType:
        if "CALL" in CallPut:
            max_ = np.max(paths, axis=0)
            payoffs = np.maximum(max_ - K, 0)
        elif "PUT" in CallPut:
            min_ = np.min(paths, axis=0)
            payoffs = np.maximum(K - min_, 0)
    elif "BARRIER" in OptionType:
        if "IN" in InOut:
            maxs = np.amax(paths, axis=0)
            paths = np.transpose(paths)
            for cnt in paths:
                if "UP" in UpDown:
                    if max(cnt) <= Barrier:
                        i = 0
                        for num in cnt:
                            cnt[i] = 0
                            i += 1
                    else:
                        None
                if "DOWN" in UpDown:
                    if min(cnt) >= Barrier:
                        i = 0
                        for num in cnt:
                            cnt[i] = 0
                            i += 1
                        # print(paths)
                    else:
                        None

        elif "OUT" in InOut:
            mins = np.amin(paths, axis=0)
            paths = np.transpose(paths)
            for cnt in paths:
                if "DOWN" in UpDown:
                    if min(cnt) <= Barrier:
                        i = 0
                        for num in cnt:
                            cnt[i] = 0
                            i += 1
                    else:
                        None
                if "UP" in UpDown:
                    if max(cnt) >= Barrier:
                        i = 0
                        for num in cnt:
                            cnt[i] = 0
                            i += 1
                    else:
                        None

        paths = np.transpose(paths)
        #print(paths)
        if "CALL" in CallPut:
            payoffs = np.maximum(paths[-1] - K, 0)
        elif "PUT" in CallPut:
            payoffs = np.maximum(K - paths[-1], 0)

    else:
        None

    # discounting back to present value
    option_price = np.mean(payoffs) * np.exp(-r * TTM)
    print(option_price)
    P = [1,N]
    P = np.ones(P)*100
    paths = np.insert(paths, 0 , P, axis=0)


    plt.plot(paths)
    plt.xlabel("Time Increments")
    plt.ylabel("Stock Price")
    plt.title("Geometric Brownian Motion")
    plt.xlim(0, n-1)       # set the xlim to left, right
    plt.show()              # Might take a while :)


monteCarloTool()


