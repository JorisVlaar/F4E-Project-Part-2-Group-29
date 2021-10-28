
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
    for i in range(periods):
        for j in range(step):
            value = ((q * values[top]) + ((1 - q) * values[top + 1])) * (1 / R)
            if prices[top - step] < value:
                values.pop(top - step)
                values.insert(top - step, value)
            top += 1
        print(values)
        top -= 2 * step
        step -= 1
    return values


def Bermudan_tree(prices, periods, ExerciseOpportunities, q, R):
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

