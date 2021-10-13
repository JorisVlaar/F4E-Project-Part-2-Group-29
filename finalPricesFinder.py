
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