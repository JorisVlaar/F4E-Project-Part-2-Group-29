import BinomialTool as BT, \
    MonteCarlo as MC
Barrier = None
InOut = None
UpDown = None
ExcerciseDates = None
decision = None
CallPut = None
K = None
OptionType = input("Enter the option type (choose from EU,US,ASIAN,BERMUDAN,CHOOSER, LOOKBACK, BARRIER): ").upper()
if "US" in OptionType:
    ToolType = "BINOMIAL"
else:
    ToolType = input("Enter the type of simulation (choose either Binomial, Monte Carlo or Both): ").upper()
P0 = int(input("Enter initial stock price: "))
if ("ASIAN" not in OptionType):
    K = int(input("Enter strike price: "))
r = float(input("Enter the annual interest rate as a decimal: "))
v = float(input("Enter the volatility as a decimal: "))
TTM = float(input("Enter the Time to Maturity in years: "))


if "BARRIER" in OptionType:
    Barrier = int(input("Enter the Barrier level: "))
    InOut = input("Enter the barrier type (choose from IN, OUT): ").upper()
    UpDown = input("Enter the barrier type (choose from UP, DOWN): ").upper()
elif "BERMUDAN" in OptionType:
    ExcerciseDates = input("Enter the period from start on which the option can be excercised. Example: 5-40-67-218. (period should be lower than 365) ")
    split = ExcerciseDates.split("-")
    decision = [int(i) for i in split]
elif "CHOOSER" in OptionType:
    decision = int(input("Enter the period from start on which the option type can be chosen. Example: 5. (should be lower than 365) "))

if not "CHOOSER" in OptionType:
    CallPut = input("Choose between: CALL, PUT ").upper()

if "BINOMIAL" in ToolType:
    if "ASIAN" or "LOOKBACK" in OptionType:
        periods = int(input("Enter the number of periods to use in the binomial simulation(for this option type the recommended amount of periods is <10): "))
    else:
        periods = int(input("Enter the number of periods to use in the binomial simulation (advised to keep below 1000): "))
    print(BT.DOBinomial(OptionType, CallPut, P0, K, v, TTM, periods, r, decision, decision, UpDown, InOut, Barrier))

elif "MONTE" and "CARLO" in ToolType:
    MC.monteCarloTool(P0, K, r, v, TTM, Barrier, OptionType, CallPut, InOut, UpDown,  decision)
elif "BOTH" in ToolType:
    if "ASIAN" or "LOOKBACK" in OptionType:
        periods = int(input("Enter the number of periods to use in the binomial simulation(for this option type the recommended amount of periods is <10): "))
    else:
        periods = int(input("Enter the number of periods to use in the binomial simulation (advised to keep below 1000): "))
    print("Binomial: ", BT.DOBinomial(OptionType, CallPut, P0, K, v, TTM, periods, r, decision, decision, UpDown, InOut, Barrier))
    MC.monteCarloTool(P0, K, r, v, TTM, Barrier, OptionType, CallPut, InOut, UpDown,  decision)

   

