# A Program to find the value of an American Put option using the binomial tree method

from Tool import finalPricesFinder as fpf
import math


def find_values(prices, PExercise):
    for i in range(len(prices)):
        if prices[i] < PExercise:
            prices[i] = (prices[i] - PExercise) * -1
        else:
            prices[i] = 0
    return prices


def find_value(prices, periods, q, R):
    step = periods
    values = list.copy(prices)
    top = len(prices) - periods - 1
    stepInverse = 2 * periods
    stepinverse2 = 0
    for i in range(periods):
        for j in range(step):
            value = ((q * values[top]) + ((1 - q) * values[top + 1])) * (1 / R)
            if prices[top - periods + stepinverse2] < value:
                values.pop(top - periods + stepinverse2)
                values.insert(top - periods + stepinverse2, value)
            top += 1
        print(values)
        step -= 1
        top -= stepInverse
        stepInverse -= 2
        stepinverse2 += 1
    return values


# inputs:
PStock = 36
PExercise = 40
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

stockPricesSimple = fpf.find_final_prices(PStock, u, d, periods)
stockPrices = fpf.find_all_prices(PStock, u, d, periods)
optionPayOff = find_values(list.copy(stockPrices), PExercise)

print(stockPricesSimple)
print(stockPrices)
print(optionPayOff)
print(find_value(optionPayOff, periods, q, R)[0])