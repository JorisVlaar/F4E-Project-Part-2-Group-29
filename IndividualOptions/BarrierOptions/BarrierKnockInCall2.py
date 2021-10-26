# A Program to find the value of an Barrier option using the binomial tree method
from Tool import findOptionPayoff as fop
import math


def find_values(prices, PExercise, option):
    if option == "Call":
        for i in range(len(prices)):
            prices[i] = max(0, prices[i] - PExercise)
    elif option == "Put":
        for i in range(len(prices)):
            prices[i] = max(0, PExercise - prices[i])
    return prices


def check(prices, PBarrier, linePosition, period, type):
    lines = find_lines(period, linePosition)
    stock = fop.find_final_prices(PStock, u, d, period)
    print("lines: " + str(lines))
    print(period)
    if type == "Down":
        prices.reverse()
    for i in range(len(prices)):
        if type == "Up" and stock[i] >= PBarrier:
            pass
        elif type == "Down" and stock[i] <= PBarrier:
            pass
        elif lines > 0:
            lines -= 1
        else:
            lines -= 1
            prices[i] = 0
    if type == "Down":
        prices.reverse()
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


def find_lines(period, linePosition):
    lines = int(period / 2)
    step = lines
    if period % 2 == 0:
        step -= 1
    for i in range(1, 1 + linePosition):
        if period % 2 == 0:
            if i % 2 == 0:
                step -= 1
            else:
                lines -= 1
        else:
            if i % 2 == 0:
                lines -= 1
            else:
                step -= 1
    return lines


def find_value(prices, PBarrier, periods, linePosition, type, q, R):
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
        step -= 1
        if i != periods - 1:
            print("step: " + str(step))
            check(values, PBarrier, linePosition, step, type)
        print(values)
        prices = list.copy(values)
        values.clear()
    return prices[0]


# inputs:
PStock = 36
PExercise = 40
PBarrier = 35
volatility = 0.4
maturity = 90 / 365
periodLength = 30 / 365
interest = 0.1
opttype = "Put"  # Option Type 'C' or 'P'
bartype = "Down"  # Barrier Type 'U' or 'D' for up or down

# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

line = find_line_position(PBarrier, PStock, u, d)
print(line)
StockPrices = fop.find_final_prices(PStock, u, d, periods)
print(StockPrices)
values = find_values(StockPrices, PExercise, opttype)
print(values)
values = check(values, PBarrier, line, periods, bartype)
print(values)
price = find_value(values, PBarrier, periods, line, bartype, q, R)
print(price)
print(periods)