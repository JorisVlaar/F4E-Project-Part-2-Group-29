
def find_values_call(prices, PExercise):
    for i in range(len(prices)):
        prices[i] = max(0, prices[i] - PExercise)
    return prices


def find_values_put(prices, PExercise):
    for i in range(len(prices)):
        prices[i] = max(0, PExercise - prices[i])
    return prices
