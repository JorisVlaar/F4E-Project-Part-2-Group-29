import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------------------------------------- #

# Standard inputs (for testing)
# P0 = 90              # initial stock price
# K = 110              # strike
# r = 0.05             # annual interest rate
# v = 0.20             # volatility
# TTM = 1              # time to maturity
# Barrier = 100        # Barrier
# OptionType = "BARRIER"
# CallPut = "PUT"
# InOut = "IN"
# UpDown = "DOWN"
# decision = "1"
# option_price = 0


# ------------------------------------------------------------------------------------------------------------- #

def simulation_path(P0, r, v, n, N,dt):
    Pt = np.log(P0) + np.cumsum(((r - ((v ** 2) / 2)) * dt +
                                 v * np.sqrt(dt) * np.random.normal(size=(n, N))), axis=0)
    return np.round_(np.exp(Pt), decimals=2)


def monteCarloTool(P0, K, r, v, TTM, Barrier, OptionType, CallPut, InOut, UpDown,  decision):
    N = 60000              # number of simulations
    n = 365                # number of steps
    dt = TTM/n
    paths = simulation_path(P0, r, v, n, N,dt)

    if "EU" in OptionType:
        if "CALL" in CallPut:
            payoffs = np.maximum(paths[-1] - K, 0)
        elif "PUT" in CallPut:
            payoffs = np.maximum(K - paths[-1], 0)
    elif "US" in OptionType:
        USr = np.power(1+r, dt)
        cnt = 0
        PVPayoffs = np.empty((n, N))
        if CallPut == "CALL":
            for step in paths:
                PVPayoffs[cnt] = (step-K)*np.power(USr, -cnt)
                cnt += 1
        elif CallPut == "PUT":
            for step in paths:
                PVPayoffs[cnt] = (K-step) * np.power(USr, -cnt)
                cnt += 1
        payoffs = np.maximum(np.amax(PVPayoffs, axis=0), 0)
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

        PotentialPayoffs = np.empty((len(decision), N))
        cnt = 0
        decision = np.array(decision) - 1
        if CallPut == "CALL":
            for period in decision:
                PotentialPayoffs[cnt] = np.maximum(
                    (paths[period]-K)*np.power(1+r, -dt * (period+1)), 0)
                cnt += 1
        elif CallPut == "PUT":
            for period in decision:
                PotentialPayoffs[cnt] = np.maximum(
                    (K - paths[period]) * np.power(1+r, -dt * (period+1)), 0)
                cnt += 1
        payoffs = np.maximum(np.amax(PotentialPayoffs, axis=0), 0)
    elif "CHOOSER" in OptionType:
        ValueIfPut = np.maximum(K-paths[decision-1], 0)
        ValueIfCall = np.maximum(paths[decision-1]-K, 0)
        payoffs = np.maximum(ValueIfPut, ValueIfCall)*np.power(r, -dt*decision)
    elif "LOOKBACK" in OptionType:
        if "CALL" in CallPut:
            max_ = np.max(paths, axis=0)
            payoffs = np.maximum(max_ - K, 0)
        elif "PUT" in CallPut:
            min_ = np.min(paths, axis=0)
            payoffs = np.maximum(K - min_, 0)
    elif "BARRIER" in OptionType:
        if "IN" in InOut:
            paths = np.transpose(paths)
            for cnt in paths:
                if "UP" in UpDown:
                    if max(cnt) <= Barrier:
                        i = 0
                        for num in cnt:
                            if "PUT" in CallPut:
                                cnt[i] = K+1
                            else:
                                cnt[i] = 0
                            i += 1
                    else:
                        None
                if "DOWN" in UpDown:
                    if min(cnt) >= Barrier:
                        i = 0
                        for num in cnt:
                            if "PUT" in CallPut:
                                cnt[i] = K+1
                            else:
                                cnt[i] = 0
                            i += 1
                        # print(paths)
                    else:
                        None

        elif "OUT" in InOut:
            paths = np.transpose(paths)
            for cnt in paths:
                if "DOWN" in UpDown:
                    if min(cnt) <= Barrier:
                        i = 0
                        for num in cnt:
                            if "PUT" in CallPut:
                                cnt[i] = K+1
                            else:
                                cnt[i] = 0
                            i += 1
                    else:
                        None
                if "UP" in UpDown:
                    if max(cnt) >= Barrier:
                        i = 0
                        for num in cnt:
                            if "PUT" in CallPut:
                                cnt[i] = K+1
                            else:
                                cnt[i] = 0
                            i += 1
                    else:
                        None

        paths = np.transpose(paths)
        # print(paths)
        if "CALL" in CallPut:
            payoffs = np.maximum(paths[-1] - K, 0)
        elif "PUT" in CallPut:
            payoffs = np.maximum(K - paths[-1], 0)

    else:
        None

    # discounting back to present value
    if "EU" in OptionType or "ASIAN" in OptionType or "LOOKBACK" in OptionType or "BARRIER" in OptionType:
        option_price = np.mean(payoffs) * np.exp(-r * TTM)
    elif "US" in OptionType or "BERMUDAN" in OptionType or "CHOOSER" in OptionType:
        option_price = np.mean(payoffs)
    
    P = [1, N]
    P = np.ones(P)*100
    paths = np.insert(paths, 0, P, axis=0)

    plt.plot(paths)
    plt.xlabel("Time Increments")
    plt.ylabel("Stock Price")
    plt.title("Geometric Brownian Motion")
    plt.xlim(0, n-1)                            # set the xlim to left, right
    plt.show()                                  # Might take a while :)

    return option_price
#monteCarloTool()
