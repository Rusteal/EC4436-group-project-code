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
#use unempployemnt as a proxy???
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
def loss(L, U0:float, Rn0:float, T:int = T, a:float = 1, b:float = 1, k:float = K, p:float = P):
    #Pi and X determined dynamically inside the loss
    #create a function like the one for shock(s) recalculate PIt for each new t inside the loop
    """idea: start in period T+1, where inflation and gap are 0, go back it time
    algebraicly derived the equation for period t loss
    Then can numerically solve the series
    L: lambda given for a particular MP committee member"""
    loss = 0
    Pi_T1 = 0
    x_T1 = 0 
    t = 20
    inflation_path = []
    output_gap_path = []
    
    while t != 0:
        
        
        t_loss = 0
        loss += t_loss
        t -= 1

# for name, L in roles.items():
#     loss(L)


def experiment(a, b, Rnt, Ut):
    return(a*Ut + b*Rnt)

#experiment 1
e1_results = []


#3.1
if __name__ == "__main__":
    #e1
    a1=[0,1,2,3]
    for a in a1:
        e1 = experiment(a, b=0, 1, 0)
    
    e1:dict = {
        
    }    

#experiment() #params for 1   
#experiment() #params for 2 etc.