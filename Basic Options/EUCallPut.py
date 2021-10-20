import numpy as np
import math 

def binomial_tree(K,TTM,P0,r,N,v,opttype='C'):
    #Calculate constants
    dt = TTM/N
    u = math.exp(v * math.sqrt(dt))     # up-factor in binomial models
    d = 1/u                             # ensure recombining tree
    q = (np.exp(r*dt) - d) / (u-d)
    disc = np.exp(-r*dt)

    # Node asset prices - Time step N
    S = np.zeros(N+1)                   # Empty array of 0s
    S[0] = P0*(d**N)
    for j in range(1,N+1):
        S[j] = S[j-1]*u/d

    # Final Option payoffs
    C = np.zeros(N+1)
    if(opttype=='C'):
        for j in range(0,N+1):
                C[j] = max(0, S[j]-K)
    if(opttype=='P'):
        for j in range(0,N+1):
                C[j] = max(0, K-S[j])

    # Iterate backwards through the tree
    for i in np.arange(N,0,-1):
        for j in range(0,i):
            C[j] = disc * ( q*C[j+1] + (1-q)*C[j] )

    return C[0]                         # Return value at t0

# Initialise parameters
P0 = 45         # initial stock price
K = 30          # strike price
TTM = 1         # time to maturity in years
r = 0.02        # annual risk-free rate
N = 3           # number of time steps
v = 0.2         # volatility
opttype = 'C'   # Option Type 'C' or 'P'

print(binomial_tree(K,TTM,P0,r,N,v,opttype='C'))