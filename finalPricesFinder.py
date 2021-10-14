
def find_final_price(price, u, d, periods):
    finalPrices = []
    iterPrice = price
    for i in range(periods):
        iterPrice = iterPrice * u
    finalPrices.append(iterPrice)
    for i in range(periods):
        iterPrice = (iterPrice / u) * d
        finalPrices.append(iterPrice)
    return finalPrices


def find_all_prices(price, u, d, periods):
    prices = [price]
    stepPrice = price
    for i in range(periods):
        stepPrice = stepPrice * u
        prices.append(stepPrice)
        iterPrice = stepPrice
        for j in range(i + 1):
            iterPrice = (iterPrice / u) * d
            prices.append(iterPrice)
    return prices