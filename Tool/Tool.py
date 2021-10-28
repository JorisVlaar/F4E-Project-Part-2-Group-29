
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
periodLength = 18.25 / 365
interest = 0.1

# computed values:
periods = int(maturity / periodLength)
u = math.exp(volatility * math.sqrt(periodLength))
d = 1 / u
R = math.exp(interest * periodLength)
q = (R - d) / (u - d)

# Specific input
OptionType = "Barrier"
CallPut = "Call"
decisionPeriod = 2
ExerciseOpportunities = []
UpDown = 'Up'
InOut = 'In'
Barrier = 35

OptionPrice = None

if OptionType == "EU":
    if CallPut == "Call":
        StockPrices = FPF.find_final_prices(PStock, u, d, periods)
        MaturityValues = FV.find_values_call(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
    elif CallPut == "Put":
        StockPrices = FPF.find_final_prices(PStock, u, d, periods)
        MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
elif OptionType == "US":
    if CallPut == "Call":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        MaturityValues = FV.find_values_call(StockPrices, PExercise)
        OptionPrice = BT.American_tree(MaturityValues, periods, q, R)
    elif CallPut == "Put":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.American_tree(MaturityValues, periods, q, R)
elif OptionType == "Asian":
    if CallPut == "Call":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        PExercise = F.find_asian_exercise_price(StockPrices)
        MaturityValues = FV.find_values_call(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
    elif CallPut == "Put":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        PExercise = F.find_asian_exercise_price(StockPrices)
        MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
elif OptionType == "Bermudan":
    if CallPut == "Call":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        MaturityValues = FV.find_values_call(StockPrices, PExercise)
        OptionPrice = BT.Bermudan_tree(MaturityValues, periods, ExerciseOpportunities, q, R)
    elif CallPut == "Put":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.Bermudan_tree(MaturityValues, periods, ExerciseOpportunities, q, R)
elif OptionType == "Chooser":
    StockPrices = FPF.find_final_prices(PStock, u, d, periods)
    optionPayOffCall = FV.find_values_call(list.copy(StockPrices), PExercise)
    optionPayOffPut = FV.find_values_put(list.copy(StockPrices), PExercise)
    valuesBefore = F.value_chooser_before(optionPayOffCall, optionPayOffPut, periods, decisionPeriod, q, R)
    OptionPrice = BT.basic_tree(valuesBefore, decisionPeriod, q, R)
elif OptionType == "LookBack":
    if CallPut == "Call":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        PExercise = F.find_lookBackCall_exercise_price(StockPrices, periods)
        MaturityValues = FV.find_values_call(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
    elif CallPut == "Put":
        StockPrices = FPF.find_all_prices(PStock, u, d, periods)
        PExercise = F.find_lookBackPut_exercise_price(StockPrices, periods)
        MaturityValues = FV.find_values_put(StockPrices, PExercise)
        OptionPrice = BT.basic_tree(MaturityValues, periods, q, R)
elif OptionType == "Barrier":
    if InOut == "Out":
        OptionPrice = B.binomial_tree_barrier(PExercise, maturity, PStock, interest, periods, Barrier, volatility, CallPut, UpDown)
    elif InOut == "In":
        OutPrice = B.binomial_tree_barrier(PExercise, maturity, PStock, interest, periods, Barrier, volatility, CallPut, UpDown)
        if CallPut == "Call":
            StockPrices = FPF.find_final_prices(PStock, u, d, periods)
            MaturityValues = FV.find_values_call(StockPrices, PExercise)
            EUPrice = BT.basic_tree(MaturityValues, periods, q, R)
        elif CallPut == "Put":
            StockPrices = FPF.find_final_prices(PStock, u, d, periods)
            MaturityValues = FV.find_values_put(StockPrices, PExercise)
            EUPrice = BT.basic_tree(MaturityValues, periods, q, R)
        OptionPrice = EUPrice - OutPrice

print(OptionPrice)