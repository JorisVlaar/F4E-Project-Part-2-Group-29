# A Program to find the value of an Bermudan Put option using the binomial tree method

from Tool import findStockPrices as fsp
import math


def find_values(prices, PExercise):
    for i in range(len(prices)):
        if prices[i] < PExercise:
            prices[i] = (prices[i] - PExercise) * -1
        else:
            prices[i] = 0
    return prices


def find_value(prices, periods, ExerciseOpportunities, q, R):
    step = periods
    values = list.copy(prices)
    top = len(prices) - periods - 1
    for i in range(periods):
        for j in range(step):
            value = ((q * values[top]) + ((1 - q) * values[top + 1])) * (1 / R)
            if prices[top - step] < value or (step - 1) not in ExerciseOpportunities:
                values.pop(top - step)
                values.insert(top - step, value)
            top += 1
        print(values)
        top -= 2 * step
        step -= 1
    return values


# inputs:
PStock = 36
PExercise = 40
volatility = 0.4
maturity = 90 / 365
periodLength = 30 / 365
interest = 0.1
ExerciseOpportunities = [1, 3]

# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

stockPricesSimple = fsp.find_final_prices(PStock, u, d, periods)
stockPrices = fsp.find_all_prices(PStock, u, d, periods)
optionPayOff = find_values(list.copy(stockPrices), PExercise)

print(stockPricesSimple)
print(stockPrices)
print(optionPayOff)
print(find_value(optionPayOff, periods, ExerciseOpportunities, q, R)[0])