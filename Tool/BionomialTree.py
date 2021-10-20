
def basic_tree(prices, periods, q, R):
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
    return prices[0]


def American_tree(prices, periods, q, R):
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
    return values[0]


def Bermudan_tree(prices, periods, ExerciseOpportunities, q, R):
    step = opportunityCheck = periods
    values = list.copy(prices)
    top = len(prices) - periods - 1
    stepInverse = 2 * periods
    stepinverse2 = 0
    for i in range(periods):
        opportunityCheck -= 1
        for j in range(step):
            value = ((q * values[top]) + ((1 - q) * values[top + 1])) * (1 / R)
            if prices[top - periods + stepinverse2] < value or opportunityCheck not in ExerciseOpportunities:
                values.pop(top - periods + stepinverse2)
                values.insert(top - periods + stepinverse2, value)
            top += 1
        print(values)
        step -= 1
        top -= stepInverse
        stepInverse -= 2
        stepinverse2 += 1
    return values[0]


def Chooser_tree(prices, periods, decision, q, R):
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

