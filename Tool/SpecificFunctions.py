import BionomialTree as BT


def find_asian_exercise_price(prices):
    PExercise = 0
    for i in range(len(prices)):
        PExercise += prices[i]
    return PExercise / len(prices)


def value_chooser_before(pricesCall, pricesPut, periods, decision, q, R):
    values = []
    valuesIFCall = BT.Chooser_tree(pricesCall, periods, decision, q, R)
    valuesIFPut = BT.Chooser_tree(pricesPut, periods, decision, q, R)
    for i in range(len(valuesIFCall)):
        if valuesIFCall[i] > valuesIFPut[i]:
            values.append(valuesIFCall[i])
        else:
            values.append(valuesIFPut[i])
    return values

#lookback functions

def find_Lookback_exercise_price_Call(prices, periods):
    index = len(prices) - (2 * periods) - 1
    indices = []
    for i in range(len(prices) - periods - 1, len(prices)):
        indices.append(possible_Call(periods, index, i))
    indices[len(indices) - 1] = indices[len(indices) - 2]
    return indices

def find_values_Lookback_Call(prices, allprices, exerciseIndex):
    print(prices)
    for i in range(len(prices)):
        print(exerciseIndex[i])
        print(allprices[exerciseIndex[i]])
        if prices[i] > allprices[exerciseIndex[i]]:
            prices[i] = prices[i] - allprices[exerciseIndex[i]]
        else:
            prices[i] = 0
    return prices

def possible_Call(period, index, position):
    nextPeriod = period - 1
    if position - period == index + nextPeriod + 1:
        return position
    position = position - period
    index -= nextPeriod
    return possible_Call(nextPeriod, index, position)



def find_values_Lookback_Put(prices, allprices, exerciseIndex):
    for i in range(len(prices)):
        if prices[i] < allprices[exerciseIndex[i]]:
            prices[i] = allprices[exerciseIndex[i]] - prices[i]
        else:
            prices[i] = 0
    return prices


def find_exercise_price_Lookback_Put(prices, periods):
    index = len(prices) - (2 * periods) - 1
    indices = []
    for i in range(len(prices) - periods - 1, len(prices)):
        indices.append(possible_Put(periods, index, i))
    indices[0] = indices[1]
    return indices


def possible_Put(period, index, position):
    nextPeriod = period - 1
    if position - period == index:
        return position
    position = position - period - 1
    index -= nextPeriod
    return possible_Put(nextPeriod, index, position)
