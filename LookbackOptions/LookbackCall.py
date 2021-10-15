# A Program to find the value of an Lookback Call option using the binomial tree method
import finalPricesFinder as fpf
import math


def find_values(prices, PExercise):
    for i in range(len(prices)):
        if prices[i] > PExercise:
            prices[i] = prices[i] - PExercise
        else:
            prices[i] = 0
    return prices


def find_exercise_price(prices, periods):
    PExercise = 0
    for i in range(len(prices) - periods - 1):
        print(prices[i])
        if i == 0:
            PExercise = prices[i]
        elif prices[i] < PExercise:
            PExercise = prices[i]
    #PExercise == prices[len(prices) - periods - 2]
    return PExercise


def find_value(prices, periods, q, R):
    step = periods
    values = []
    for i in range(periods):
        top = 0
        bottom = top + 1
        for j in range(step):
            value = ((q * prices[top]) + ((1 - q) * prices[bottom])) * (1 / R)
            values.append(value)
            top = bottom
            bottom += 1
        print(values)
        prices = list.copy(values)
        values.clear()
        step -= 1
    return prices


# inputs:
PStock = 36
volatility = 0.4
maturity = 90 / 365
periodLength = 30 / 365
interest = 0.1

# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

stockPrices = fpf.find_all_prices(PStock, u, d, periods)

PExercise = find_exercise_price(stockPrices, periods)
print(PExercise)

optionPayOff = find_values(list.copy(stockPrices), PExercise)

print(stockPrices)
print(optionPayOff)
print(find_value(optionPayOff, periods, q, R)[0])
