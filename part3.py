"""
Parameter Symbol Value
Discount factor 𝛽 0.99
Inverse intertemporal elasticity of substitution 𝜎 1.0
Slope of the Phillips curve 𝜅 0.13
Shock persistence 𝜌 0.20
Horizon (quarters) 𝑇 20"""

#need to calculate shocks, get data for PIt, E(PIt+1), Xt, It, E(Xt+1)
#normilise data to quoterly and mena deviation
#report *4 in annual terms

#evaluate rules
#experiments

BETA = .99
SIGMA = 1
K = .13
P  = .2
T = 20

#ideally have data for q3, expected inflation can be for q4? q1? Avarage of those? Hard to pin down
gap = -1.1 # table says no convertion, makes sence if you think about it
E_gap = -1.1 # not sure where to get, OBR has -1.1 for all future, futher forcast is not specified
PIt = (3.17 - 2)/4 
E_PIt1 = (5-2)/4
It = (3.75/4 - 1.25/4 - 0.5) #should be at neutral lvl, taken from the table page 4 of the brief

def idendify_cost_push_shock_q(PIt, E_PIt1, Xt, beta=BETA, k=K) -> float:
    return(PIt - beta*E_PIt1 - k*Xt)

def idendify_demand_shock_q(It, E_PIt1, Xt, E_Xt1, sigma=SIGMA) -> float:
    return(It - E_PIt1 + sigma*(Xt-E_Xt1))

Ut = 4*idendify_cost_push_shock_q(PIt, E_PIt1, gap)
Rnt = 4*idendify_demand_shock_q(It, E_PIt1, gap, E_gap)
print(f"Annual identified cost push shock pp: {Ut}") # -1.22799999999
print(f"Annual identified demand shock pp: {Rnt}") #-2.5
#not sure about values tbh, expected inflation arbitrary, taken from the monetary policy public statement

#now experiements

roles: dict = {
'hank': 0.05, 
'hankish centrist':.1, 
'balanced':.25,
'dove':1}

#evaluate a and b
#need to minimise this function. Not sure how to do that in python
#there is a function in sci py http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
def loss(L, T:int = T):
    #Pi and X determined dunamically inside the loss
    PIt = 0 #create a function like the one for shock(s) recalculate PIt for each new t inside the loop
    Xt = 0 
    total_loss = 0
    for t in range(1, T+1):
        total_loss += PIt^2 + L*Xt

for name, L in roles.items():
    loss(L)


def experiment(a, b, Rnt, Ut):
    return(a*Ut + b*Rnt)

#experiment 1
e1_results = []

#experiment()    