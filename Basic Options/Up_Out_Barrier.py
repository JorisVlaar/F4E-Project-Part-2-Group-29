import numpy as np
import math
# Initialise parameters
P0 = 100      # initial stock price
K = 110       # strike price
TTM = 1       # time to maturity in years
r = 0.1      # annual risk-free rate
N = 21         # number of time steps
v = 0.25       # volatility
B = 125        # Up and out Barrier
opttype = 'P'  # Option Type 'C' or 'P'


def binomial_tree_barrier(K, TTM, P0, r, N, B, v, opttype):
    # Calculate constants
    dt = TTM/N
    u = math.exp(v * math.sqrt(dt))  # up-factor in binomial models
    d = 1/u                          # ensure recombining tree
    q = (np.exp(r*dt) - d) / (u-d)
    disc = np.exp(-r*dt)             # discounted rate

    # Matuarity asset prices - Time step N
    S = np.zeros(N+1)  # empty array of 0s
    for j in range(0, N+1):
        S[j] = P0 * (u**j) * (d**(N-j))

    # Option payoffs
    C = np.zeros(N+1)  # empty array of 0s
    if(opttype == 'C'):
        for j in range(0, N+1):
            C[j] = max(0, S[j]-K)
    if(opttype == 'P'):
        for j in range(0, N+1):
            C[j] = max(0, K-S[j])
    # Check condition payoff
    for j in range(0, N+1):
        S = P0 * u**j * d**(N-j)
        if S >= B:
            C[j] = 0

    # Iterate backwards through the tree
    for i in np.arange(N-1, -1, -1):
        for j in range(0, i+1):
            S = P0 * u**j * d**(i-j)
            if S >= B:
                C[j] = 0
            else:
                C[j] = disc * (q*C[j+1]+(1-q)*C[j])

    return C[0]
print(binomial_tree_barrier(K, TTM, P0, r, 400, B, v, opttype))

# i = 1
# while(i < 1000):
#     print(binomial_tree_barrier(K, TTM, P0, r, i, B, v, opttype))
#     i = i+1
