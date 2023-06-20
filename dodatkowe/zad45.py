from scipy.optimize import minimize

def S_function(s, k, m):
    return 1 - (1 - s**k)**m

target_values = [(1/3, 1/10), (1/2, 9/10)]

for s, target in target_values:
    objective = lambda x: abs(S_function(s, x[0], x[1]) - target)
    result = minimize(objective, [0.5, 0.5], method='SLSQP', bounds=[(0, 100), (0, 1000)])
    k = result.x[0]
    m = result.x[1]
    print(f"Wyliczona wartość: {S_function(s,k,m)}")
    print(f"S({s},{k},{m}) ~ {target}")
