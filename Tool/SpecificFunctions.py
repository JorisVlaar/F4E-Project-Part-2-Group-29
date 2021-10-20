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


def find_lookBackCall_exercise_price(prices, periods):
    PExercise = 0
    for i in range(len(prices) - periods - 1):
        if i == 0:
            PExercise = prices[i]
        elif prices[i] < PExercise:
            PExercise = prices[i]
    return PExercise

def find_lookBackPut_exercise_price(prices, periods):
    PExercise = 0
    for i in range(len(prices) - periods - 1):
        if i == 0:
            PExercise = prices[i]
        elif prices[i] > PExercise:
            PExercise = prices[i]
    return PExercise