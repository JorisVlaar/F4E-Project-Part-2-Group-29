# A Program to find the value of a Barrier Knock-In Call option using the binomial tree method
import finalPricesFinder as fpf
import math


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


def some_name(prices, periods, KIPrice, PStock, linePosition):
    lines = int(periods/2)
    step = lines
    if periods % 2 == 0:
        step -= 1

    for i in range(1, 1+ linePosition):
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
    print(lines)
    print(step)
    print("------------------------")
    actualPrices = []
    if KIPrice > PStock:
        index = 0
        for k in prices:
            if k >= KIPrice:
                actualPrices.append(k)
                index += 1
        linesCopy = lines
        for i in range(linesCopy):
            actualPrices.append(find_paths_via(lines, step) / find_paths(periods)[index] * prices[index])
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
                actualPrices.append(k)
                index -= 1
        actualPrices.reverse()
        linesCopy = lines
        for i in range(linesCopy):
            print(find_paths_via(lines, step))
            print(find_paths(periods)[index])
            print(prices[index])
            print("------------------------")
            actualPrices.append(find_paths_via(lines, step) / find_paths(periods)[index] * prices[index])
            index -= 1
            lines -= 1
            step += 1
            if lines == 1:
                step = 0
        for j in range(len(actualPrices), len(prices)):
            actualPrices.append(0)
        actualPrices.reverse()
        return actualPrices


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


def find_values(prices, PExercise):
    for i in range(len(prices)):
        if prices[i] > PExercise:
            prices[i] = prices[i] - PExercise
        else:
            prices[i] = 0
    return prices


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
PExercise = 40
KnockInPrice = 41
volatility = 0.4
maturity = 180 / 365
periodLength = 30 / 365
interest = 0.1

# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

print(fpf.find_all_prices(PStock, u, d, periods))
position = find_line_position(KnockInPrice, PStock, u, d)
print("------------------------")
prices = some_name(fpf.find_final_prices(PStock, u, d, periods), periods, KnockInPrice, PStock, position)
print(prices)
print(position)
print(find_value(find_values(prices, PExercise), periods, q, R))
