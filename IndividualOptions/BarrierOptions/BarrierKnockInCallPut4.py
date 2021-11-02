# A Program to find the value of an EU Call option using the binomial tree method
from Tool import findStockPrices as fsp
import math


def find_values(prices, PExercise, option):
    if option == "Call":
        for i in range(len(prices)):
            prices[i] = max(0, prices[i] - PExercise)
    elif option == "Put":
        for i in range(len(prices)):
            prices[i] = max(0, PExercise - prices[i])
    return prices


def find_value(prices, periods, q, R):
    step = periods
    values = []
    for i in range(periods):
        top = 0
        for j in range(step):
            value = ((q * prices[top]) + ((1 - q) * prices[top + 1])) * (1 / R)
            values.append(value)
            top += 1
        prices = list.copy(values)
        values.clear()
        step -= 1
    return prices


def find_line_position(KIPrice, PStock, u, d):
    position = 0
    if KIPrice > PStock:
        while PStock * u < KIPrice:
            position += 1
            PStock = PStock * u
    if KIPrice < PStock:
        while PStock * d > KIPrice:
            position += 1
            PStock = PStock * d
    return position


def find_paths(periods):
    values = []
    previous = []
    for i in range(1, periods+1):
        values.append(1)
        for j in range(len(previous)-1):
            values.append(previous[j]+previous[j+1])
        values.append(1)
        previous = list.copy(values)
        values.clear()
    return previous


def find_paths_via(lines, step):
    paths = 0
    previous = []
    step2 = 0
    for i in range(1, int(lines) + 1):
        if i == 1:
            paths += 1
        elif i == 2:
            for j in range(1, step + 2):
                paths += 1
                previous.append(1)
        elif i > 2:
            for k in previous:
                step2 += k
            for j in range(0, step + 1):
                paths += step2
                pop = previous.pop(j)
                previous.insert(j, step2)
                step2 -= pop
    lines -= 1
    previous.clear()
    for i in range(1, int(lines) + 1):
        if i == 1:
            paths += 1
        elif i == 2:
            for j in range(1, step + 2):
                paths += 1
                previous.append(1)
        elif i > 2:
            for k in previous:
                step2 += k
            for j in range(0, step + 1):
                paths += step2
                pop = previous.pop(j)
                previous.insert(j, step2)
                step2 -= pop
    return paths


def some_name(prices, periods, KIPrice, PStock, linePosition):
    lines = int(periods/2)
    step = lines
    if periods % 2 == 0:
        step -= 1

    for i in range(1, 1 + linePosition):
        if periods % 2 == 0:
            if i % 2 == 0:
                step -= 1
            else:
                lines -= 1
        else:
            if i % 2 == 0:
                lines -= 1
            else:
                step -= 1
    if lines <= 0:
        lines = 0
    if step <= 0:
        step = 0
    actualPrices = []
    if KIPrice > PStock:
        index = 0
        for k in prices:
            if k >= KIPrice:
                print(find_paths(periods)[index])
                actualPrices.append(find_paths(periods)[index])
                index += 1
        linesCopy = lines
        for i in range(linesCopy):
            actualPrices.append(find_paths_via(lines, step))
            index += 1
            lines -= 1
            step += 1
            if lines == 1:
                step = 0
        for j in range(len(actualPrices), len(prices)):
            actualPrices.append(0)
        return actualPrices
    elif KIPrice < PStock:
        index = len(prices) - 1
        for k in prices:
            if k <= KIPrice:
                actualPrices.append(find_paths(periods)[index])
                index -= 1
        actualPrices.reverse()
        linesCopy = lines
        for i in range(linesCopy):
            actualPrices.append(find_paths_via(lines, step))
            index -= 1
            lines -= 1
            step += 1
            if lines == 1:
                step = 0
        for j in range(len(actualPrices), len(prices)):
            actualPrices.append(0)
        actualPrices.reverse()
        return actualPrices


def find_value_probability(prices, paths, pathsVia, R, periods):
    value = 0
    path = 0
    for i in paths:
        path += i
    for i in range(len(prices)):
        value += (prices[i] / pow(R, periods)) * (pathsVia[i]/path)
    return value

# inputs:
PStock = 41
PExercise = 37
KnockInPrice = 42
volatility = 0.4
maturity = 90 / 365
periodLength = 30 / 365
interest = 0.1
opttype = "Put"  # Option Type 'C' or 'P'

# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

stockPrices = fsp.find_final_prices(PStock, u, d, periods)
optionPayOff = find_values(list.copy(stockPrices), PExercise, opttype)

print(stockPrices)
print(optionPayOff)
print(find_value(optionPayOff, periods, q, R)[0])
print("-------")
print(some_name(stockPrices, periods, KnockInPrice, PStock, find_line_position(KnockInPrice, PStock, u, d)))
print(find_value_probability(optionPayOff, find_paths(periods), some_name(stockPrices, periods, KnockInPrice, PStock, find_line_position(KnockInPrice, PStock, u, d)), R, periods))

# value = 100000000000000000000000
# periods = 5
# while periods <= 80:
#     print(periods)
#     periodLength = maturity/periods
#     u = math.exp(volatility * math.sqrt(periodLength))
#     d = 1 / u
#     R = math.exp(interest * periodLength)
#     q = (R - d) / (u - d)
#     stockPrices = fsp.find_final_prices(PStock, u, d, periods)
#     optionPayOff = find_values(list.copy(stockPrices), PExercise, opttype)
#     value1 = find_value_probability(optionPayOff, find_paths(periods), some_name(stockPrices, periods, KnockInPrice, PStock, find_line_position(KnockInPrice, PStock, u, d)), R, periods)
#     print(value1)
#     if value1 > value:
#         value = value1
#     periods += 1
#
# print("-------")
# print(value)