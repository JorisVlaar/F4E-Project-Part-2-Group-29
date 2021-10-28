import numpy as np
import math

def binomial_tree_barrier(K, TTM, P0, r, N, B, v, opttype, bartype):
    # Calculate constants
    dt = TTM/N                          # Timesteps
    u = math.exp(v * math.sqrt(dt))     # Up-factor in binomial models
    d = 1/u                             # Ensure recombining tree
    q = (np.exp(r*dt) - d) / (u-d)
    disc = np.exp(-r*dt)                # Discounted rate

    # Node asset prices - Time step N
    S = np.zeros(N+1)                   # Empty array of 0s
    for j in range(0, N+1):             # From front to back generate values for the binomial-tree
        S[j] = P0 * (u**j) * (d**(N-j)) # Calculate value for node

    # Final Option payoffs
    C = np.zeros(N+1)                   # Empty array of 0s
    if(opttype == 'C'):                 # Check if Call/Put
        for j in range(0, N+1):         # Iterate over binomial-tree and calculate option payoff for Call
            C[j] = max(0, S[j]-K)
    elif(opttype == 'P'):
        for j in range(0, N+1):         # Iterate over binomial-tree and calculate option payoff for Put
            C[j] = max(0, K-S[j])

    # Check condition payoff
    for j in range(0, N+1):             # Iterate over array and calculate node value (underlying asset)
        S = P0 * (u**j) * (d**(N-j))
        if(bartype == 'U'):             # Check if Up/Down
            if S >= B:                  # Check if barrier is reached
                C[j] = 0                # Set payoff to 0 if barrier reached
        elif(bartype == 'D'):
            if S <= B:
                C[j] = 0

    # Iterate backwards through the tree
    for i in np.arange(N-1, -1, -1):
        for j in range(0, i+1):
            S = P0 * (u**j) * (d**(i-j))

            if(bartype == 'U'):         # Check if Up/Down
                if S >= B:              # Check if barrier is reached
                    C[j] = 0            # Set payoff to 0 if barrier reached
            else:
                  C[j] = disc * (q*C[j+1]+(1-q)*C[j])
            if(bartype == 'D'):
                if S <= B:
                    C[j] = 0
            else:
                  C[j] = disc * (q*C[j+1]+(1-q)*C[j])
    return C[0]                         # Return value at t0

def binomial_tree(K,TTM,P0,r,N,v,opttype):
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

def calculation(K, TTM, P0, r, N, B, v, opttype, bartype,bart):
    if (bart=='O'):
       return binomial_tree_barrier(K, TTM, P0, r, 38, B, v, opttype, bartype)
    elif (bart=='I'):
        return (binomial_tree(K,TTM,P0,r,N,v,opttype) - binomial_tree_barrier(K, TTM, P0, r, 38, B, v, opttype, bartype))



# Initialise parameters
P0 = 100       # initial stock price
K = 110        # strike price
TTM = 1        # time to maturity in years
r = 0.1        # annual risk-free rate
N = 21         # number of time steps
v = 0.25       # volatility
B = 125        # Up/down and out Barrier
opttype = 'P'  # Option Type 'C' or 'P'
bartype = 'U'  # Barrier Type 'U' or 'D' for up or down
bart = 'I'      # Barrier Type 'I' for knock-in 'O' for Knock-out

# Testing
print(calculation(K, TTM, P0, r, 38, B, v, opttype, bartype, bart))

# Testing
# i = 20
# while(i < 43):
#     print(binomial_tree_barrier(K, TTM, P0, r, i, B, v, 'P'))
#     i = i+1

#Testing
# i = 20
# while(i < 43):
#     print(binomial_tree_barrier(K, TTM, P0, r, i, 65, v, 'C', 'D'))
#     i = i+1
# print('help')
# i = 20
# while(i < 43):
#     print(binomial_tree_barrier(K, TTM, P0, r, i, 65, v, 'P', 'D'))
#     i = i+1
