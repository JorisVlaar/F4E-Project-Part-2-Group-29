# A Program to find the value of an Chooser option using the binomial tree method

from Tool import findOptionPayoff as fop
import math


def find_values_call(prices, PExercise):
    for i in range(len(prices)):
        if prices[i] > PExercise:
            prices[i] = prices[i] - PExercise
        else:
            prices[i] = 0
    return prices


def find_values_put(prices, PExercise):
    for i in range(len(prices)):
        if prices[i] < PExercise:
            prices[i] = (prices[i] - PExercise) * -1
        else:
            prices[i] = 0
    return prices


def find_value_before(pricesCall, pricesPut, periods, decision, q, R):
    values = []
    valuesIFCall = find_value(pricesCall, periods, decision, q, R)
    valuesIFPut = find_value(pricesPut, periods, decision, q, R)
    for i in range(len(valuesIFCall)):
        if valuesIFCall[i] > valuesIFPut[i]:
            values.append(valuesIFCall[i])
        else:
            values.append(valuesIFPut[i])
    return values


def find_value(prices, periods, decision, q, R):
    step = periods
    periods -= decision
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
PExercise = 40
volatility = 0.4
maturity = 90 / 365
periodLength = 30 / 365
interest = 0.1
decisionPeriod = 2

# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

# rounded values for checking
u = 1.0748
d = 0.9304
q = 0.4993
print(find_value([4.1280, 4.8504, 12.2398], decisionPeriod, 0, q, R)[0])

stockPrices = fop.find_final_prices(PStock, u, d, periods)
optionPayOffCall = find_values_call(list.copy(stockPrices), PExercise)
optionPayOffPut = find_values_put(list.copy(stockPrices), PExercise)

print(stockPrices)
print(optionPayOffCall)
valuesBefore = find_value_before(optionPayOffCall, optionPayOffPut, periods, decisionPeriod, q, R)
print(valuesBefore)
print(find_value(valuesBefore, decisionPeriod, 0, q, R)[0])

