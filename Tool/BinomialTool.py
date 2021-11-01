
import math
import BionomialTree as BT, \
    findStockPrices as FPF, \
    findOptionPayoff as FV, \
    SpecificFunctions as F, \
    BarrierOptions as B

# basic inputs:
PStock = 38
PExercise = 38
volatility = 0.4
maturity = 365 / 365
periods = 20
periodLength = 18.25 / 365
interest = 0.1

# Specific input
OptionType = "BARRIER"
CallPut = "Call"
decisionPeriod = 2
ExerciseOpportunities = []
UpDown = 'Up'
InOut = 'In'
Barrier = 35


def DOBinomial(OptionType, CallPut, PStock, PExercise, volatility, maturity, periods, interest, decisionPeriod, ExerciseOpportunities, UpDown, InOut, Barrier):

    # computed values:
    periodLength = maturity / periods
    u = math.exp(volatility * math.sqrt(periodLength))
    d = 1 / u
    R = math.exp(interest * periodLength)
    q = (R - d) / (u - d)
    OptionPrice = None
    MaturityValues = None

    if OptionType == "EU":
        StockPrices = FPF.find_final_prices(PStock, u, d, periods)
        if CallPut == "CALL":
            MaturityValues = FV.find_values_call(StockPrices, PExercise)
        elif CallPut == "PUT":
            MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
    elif OptionType == "US":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        if CallPut == "CALL":
            MaturityValues = FV.find_values_call(StockPrices, PExercise)
        elif CallPut == "PUT":
            MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.American_tree(MaturityValues, periods, q, R)
    elif OptionType == "ASIAN":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        PExercise = F.find_asian_exercise_price(StockPrices)
        if CallPut == "CALL":
            MaturityValues = FV.find_values_call(StockPrices, PExercise)
        elif CallPut == "PUT":
            MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
    elif OptionType == "BERMUDAN":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        if CallPut == "CALL":
            MaturityValues = FV.find_values_call(StockPrices, PExercise)
        elif CallPut == "PUT":
            MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.Bermudan_tree(MaturityValues, periods, ExerciseOpportunities, q, R)
    elif OptionType == "CHOOSER":
        StockPrices = FPF.find_final_prices(PStock, u, d, periods)
        optionPayOffCall = FV.find_values_call(list.copy(StockPrices), PExercise)
        optionPayOffPut = FV.find_values_put(list.copy(StockPrices), PExercise)
        valuesBefore = F.value_chooser_before(optionPayOffCall, optionPayOffPut, periods, decisionPeriod, q, R)
        OptionPrice = BT.basic_tree(valuesBefore, decisionPeriod, q, R)
    elif OptionType == "LOOKBACK":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        PExercise = F.find_lookBackCall_exercise_price(StockPrices, periods)
        if CallPut == "CALL":
            MaturityValues = FV.find_values_call(StockPrices, PExercise)
        elif CallPut == "PUT":
            MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
    elif OptionType == "BARRIER":
        OptionPrice = B.binomial_tree_barrier(PExercise, maturity, PStock, interest, periods, Barrier, volatility, CallPut, UpDown)
        if InOut == "IN":
            StockPrices = FPF.find_final_prices(PStock, u, d, periods)
            if CallPut == "CALL":
                MaturityValues = FV.find_values_call(StockPrices, PExercise)
            elif CallPut == "PUT":
                MaturityValues = FV.find_values_put(StockPrices, PExercise)
            EUPrice = BT.basic_tree(MaturityValues, periods, q, R)
            OptionPrice = EUPrice - OptionPrice
    return OptionPrice

#print(DOBinomial(OptionType, CallPut, PStock, PExercise, volatility, maturity, periods, interest, decisionPeriod, ExerciseOpportunities, UpDown, InOut, Barrier))
