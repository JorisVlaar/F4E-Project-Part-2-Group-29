
from Tool import finalPricesFinder as fpf
import math

def find_values(prices, PExercise, option):
    if option == "Call":
        for i in range(len(prices)):
            prices[i] = max(0, prices[i] - PExercise)
    elif option == "Put":
        for i in range(len(prices)):
            prices[i] = max(0, PExercise - prices[i])
    return prices


def check(prices, periods, period, type, stock, index, barrier, u, d):
    for i in range(len(prices)):
        position = index + period + i
        if type == "Up" and stock[position] >= PBarrier:
            pass
        elif type == "Down" and stock[position] <= PBarrier:
            pass
        else:
            test_after = possible(period, type, stock, index, barrier, position)
            test_before = possible_before(periods, period, stock[position], barrier, type, u, d)
            if test_after or test_before:
                pass
            else:
                prices[i] = 0
    return prices


def possible(period, type, stock, index, barrier, position):
    nextPeriod = period - 1
    if type == "Up" and position - period == index or type == "Down" and position - period == index + nextPeriod + 1:
        return False
    for j in range(index, index + nextPeriod + 1):
        if type == "Up" and stock[j] >= barrier and position - period - 1 == j:
            return True
        elif type == "Down" and stock[j] <= barrier and position - period == j:
            return True
    if type == "Up":
        position = position - period - 1
    elif type == "Down":
        position = position - period
    index -= nextPeriod
    return possible(nextPeriod, type, stock, index, barrier, position)


def possible_before(periods, period, PStock, barrier, type, u, d):
    if type == "Up":
        for i in range(period, periods):
            PStock = PStock*u
        if PStock>=barrier:
            return True
        else:
            return False
    elif type == "Down":
        for i in range(period, periods):
            PStock = PStock*d
        if PStock<=barrier:
            return True
        else:
            return False



def find_value(prices, periods, q, R, type, stock, index, barrier, u ,d):
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
        #print(values)
        if i != periods - 1:
            #print("step: " + str(step))
            #print("index: " + str(index))
            values = check(values, periods, step, type, stock, index, barrier, u, d)
            index = index - step + 1
        step -= 1
        #print(values)
        prices = list.copy(values)
        values.clear()
    return prices[0]


# inputs:
PStock = 42
PExercise = 45
PBarrier = 70
volatility = 0.4
maturity = 1
periodLength = 1
interest = 0.1
opttype = "Put"  # Option Type 'C' or 'P'
bartype = "Up"  # Barrier Type 'U' or 'D' for up or down

# # computed values:
# periods = int(maturity / periodLength)
# u = math.exp(volatility * math.sqrt(periodLength))
# d = 1 / u
# R = math.exp(interest * periodLength)
# q = (R - d) / (u - d)
#
# stockPrices = fpf.find_all_prices(PStock, u, d, periods)
# optionPayOff = find_values(fpf.find_final_prices(PStock, u, d, periods), PExercise, opttype)
#
# index = len(stockPrices) - (2*periods) - 1

#print(stockPrices)
#print(find_value(optionPayOff, periods, q, R, bartype, stockPrices, index, PBarrier))

periods = 5
while periods <= 80:
    print(periods)
    periodLength = maturity/periods
    u = math.exp(volatility * math.sqrt(periodLength))
    d = 1 / u
    R = math.exp(interest * periodLength)
    q = (R - d) / (u - d)
    stockPrices = fpf.find_all_prices(PStock, u, d, periods)
    #print(stockPrices)
    optionPayOff = find_values(fpf.find_final_prices(PStock, u, d, periods), PExercise, opttype)
    #print(optionPayOff)
    index = len(stockPrices) - (2 * periods) - 1
    print(find_value(optionPayOff, periods, q, R, bartype, stockPrices, index, PBarrier, u, d))
    #print("--------------"+str(periods+1)+"---------------")
    periods += 1

