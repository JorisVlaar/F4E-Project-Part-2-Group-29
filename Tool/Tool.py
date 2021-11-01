import BinomialTool as BT, \
    MonteCarlo as MC
Barrier = None
InOut = None
UpDown = None
ExcerciseDates = None
decision = None
ToolType = input("Enter the type of simulation (choose either Binomial or Monte Carlo:").upper()
P0 = int(input("Enter initial stock price: "))
K = int(input("Enter strike price: "))
r = float(input("Enter the annual interest rate as a decimal: "))
v = float(input("Enter the volatility as a decimal: "))
TTM = float(input("Enter the Time to Maturity in years: "))

OptionType = input("Enter the option type (choose from EU,US,ASIAN,BERMUDAN,CHOOSER, LOOKBACK, BARRIER): ").upper()
if "BARRIER" in OptionType:
    Barrier = int(input("Enter the Barrier level: "))
    InOut = input("Enter the barrier type (choose from IN, OUT): ").upper()
    UpDown = input("Enter the barrier type (choose from UP, DOWN): ").upper()
elif "BERMUDAN" in OptionType:
    ExcerciseDates = input("Enter the day from start on which the option can be excercised. Example: 5-40-67-218.  ")
    decision = ExcerciseDates.split("-")
elif "CHOOSER" in OptionType:
    ExcerciseDates = input("Enter the period from start on which the option can be excercised. Example: 5.  ")
    decision = ExcerciseDates
CallPut = input("Choose between: CALL, PUT ").upper()
if ToolType == "BINOMIAL":
    periods = int(input("Enter the amount of periods to use in the simulation:"))
    OptionPrice = BT.DOBinomial(OptionType, CallPut, P0, K, v, TTM, periods, r, decision, decision, UpDown, InOut, Barrier)
elif ToolType == "MONTE CARLO":
    OptionPrice = MC.monteCarloTool(P0, K, r, v, TTM, Barrier, OptionType, CallPut, InOut, UpDown,  decision)
print(OptionPrice)

