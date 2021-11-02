# A Program to find the value of an Lookback Call option using the binomial tree method
from Tool import findStockPrices as fsp
import math


def find_values(prices, allprices, exerciseIndex):
    print(prices)
    for i in range(len(prices)):
        print(exerciseIndex[i])
        print(allprices[exerciseIndex[i]])
        if prices[i] > allprices[exerciseIndex[i]]:
            prices[i] = prices[i] - allprices[exerciseIndex[i]]
        else:
            prices[i] = 0
    return prices


def find_exercise_price(prices, periods):
    index = len(prices) - (2 * periods) - 1
    indices = []
    for i in range(len(prices) - periods - 1, len(prices)):
        indices.append(possible(periods, index, i))
    indices[len(indices) - 1] = indices[len(indices) - 2]
    return indices


def possible(period, index, position):
    nextPeriod = period - 1
    if position - period == index + nextPeriod + 1:
        return position
    position = position - period
    index -= nextPeriod
    return possible(nextPeriod, index, position)

def find_value(prices, periods, q, R):
    step = periods
    values = []
    for i in range(periods):
        top = 0
        for j in range(step):
            value = ((q * prices[top]) + ((1 - q) * prices[top + 1])) * (1 / R)
            values.append(value)
            top += 1
        print(values)
        prices = list.copy(values)
        values.clear()
        step -= 1
    return prices


# inputs:
PStock = 100
volatility = 0.4
maturity = 1
periodLength = 0.02
interest = 0.1


# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

stockPrices = fsp.find_all_prices(PStock, u, d, periods)

PExercise = find_exercise_price(stockPrices, periods)
print(PExercise)

optionPayOff = find_values(fsp.find_final_prices(PStock, u, d, periods), list.copy(stockPrices), PExercise)

# print(stockPrices)
print(optionPayOff)
print(find_value(optionPayOff, periods, q, R)[0])
