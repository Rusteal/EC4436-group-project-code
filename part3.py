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
E_gap = -1.0 # not sure where to get, OBR has -1.1 for all future, futher forcast is not specified
#-1.0 figure exists in Monetary policy report, prediction for Q4 2026
#use unempployemnt as a proxy??? have justification, flat projection in OBR up until mid 2027, report made in Oct26
PIt = (3.17 - 2)/4 
E_PIt1 = (2.5-2)/4 #to change based on data. OBE, q4 2027 is 4%, if have 4%, rates are negative, so use 2.5; median MAPS is 2.5, questioneer
POLICY_RATE = 3.75
It = (POLICY_RATE/4 - 1.25/4 - 0.5) #should be at neutral lvl, taken from the table page 4 of the brief, actually evaluates to 0

def idendify_cost_push_shock_q(PIt, E_PIt1, Xt, beta=BETA, k=K) -> float:
    return(PIt - beta*E_PIt1 - k*Xt)

def idendify_demand_shock_q(It, E_PIt1, Xt, E_Xt1, sigma=SIGMA) -> float:
    return(It - E_PIt1 + sigma*(Xt-E_Xt1))

Ut = idendify_cost_push_shock_q(PIt, E_PIt1, gap)
Rnt = idendify_demand_shock_q(It, E_PIt1, gap, E_gap)
print(f"Annual identified cost push shock pp: {Ut*4}") 
print(f"Annual identified demand shock pp: {Rnt*4}") 

#now experiements
#before need to find optimal a,b; later noticed that in c) supposed to find a,b thorugh looking into loss tables,
#but did optimisation below instead, more rigorous, allows for globally optimal a,b instead of best of the list

roles: dict = {
'hawk': {'lambda':0.05, 'a':0, 'b':0}, 
'hawkish centrist': {'lambda':.1, 'a':0, 'b':0}, 
'balanced':{'lambda':0.25, 'a':0, 'b':0},
'dove':{'lambda':1, 'a':0, 'b':0}}

#evaluate a and b
#need to minimise this function. Not sure how to do that in python
#there is a function in sci py http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
def loss(L, U0:float, Rn0:float, T:int = T, a:float = 1, b:float = 1, k:float = K, p:float = P) -> tuple[float, list, list]:
    #Pi and X determined dynamically inside the loss
    #create a function like the one for shock(s) recalculate PIt for each new t inside the loop
    """idea: start in period T+1, where inflation and gap are 0, go back it time
    algebraicly derived the equation for period t loss
    Then can numerically solve the series for optimal a,b 
    L: lambda given for a particular MP committee member"""
    loss = 0
    Pi_T1 = 0
    x_T1 = 0 
    t = T
    
    
    inflation_path = []
    output_gap_path = []
    
    def loss_t(PIt1, Xt1, Ut, RNt, t, L) -> tuple[float, float, float]:
        """returns 1) loss; 2) current inflation; 3) current gap  """
        xt = Xt1 + (PIt1+ (1-b)*RNt - a*Ut)/SIGMA
        PIt = BETA*PIt1 + K*xt + Ut
        return (PIt**2 + L*(xt**2), PIt, xt)
    
    while t != 0:
        t_loss = loss_t(Pi_T1, x_T1, ((p**(t-1))*U0), ((p**(t-1))*Rn0), t, L)
        inflation_path.append(t_loss[1])
        output_gap_path.append(t_loss[2])
        loss += t_loss[0]
        Pi_T1 = t_loss[1]
        x_T1 = t_loss[2]
        t -= 1
        
    inflation_path.reverse()
    output_gap_path.reverse()
        
    return (loss, inflation_path, output_gap_path)

import pandas as pd
#will be used a few times, so easier with a function
def roles_to_csv(roles:dict, csv_name:str) -> pd.DataFrame:
    
    df = pd.DataFrame.from_dict(roles, orient="index")
    df.index.name = "role"
    df = df.reset_index()
    df.to_csv(csv_name, index=False, float_format="%.3f")
    return df
    
if __name__ == "__main__":
    #Experiment 3 extended, globally optimal a,b
    def find_optimal_a_b_all_roles(roles:dict, U0, Rn0, p:float=P, save_to_csv:bool = True, csv_name:str = "roles_a_b.csv")-> dict:
        roles_local = roles.copy()
        for name, dict in roles_local.items():
            from scipy.optimize import minimize 
            min_a_b = minimize(fun=lambda params: loss(dict['lambda'], U0, Rn0, p=p, a=params[0],b=params[1])[0], x0=[1.0, 1.0])
            a_optimal, b_optimal = min_a_b.x
            roles_local[name]['a'] = a_optimal
            roles_local[name]['b'] = b_optimal
            #diagnostics, can be commneted out
            print(f"{name}:")
            print(f"  a = {a_optimal:.4f}")
            print(f"  b = {b_optimal:.4f}")
            print(f"  Loss = {min_a_b.fun:.6f}")
            print(f"  Converged = {min_a_b.success}")
        
        if save_to_csv:
            roles_to_csv(roles_local, csv_name)
        
        return roles_local
    
    #Experiment 3 run
    roles_p_2 = find_optimal_a_b_all_roles(roles, Ut, Rnt, save_to_csv=False,  csv_name="roles_a_b_p=.2.csv")
    def optimal_i(Rnt, Ut, a, b)-> float:
        return a*Ut*4 + b*Rnt*4
    
    # find appropriate i
    optimal_i_for_roles = []
    
    for role, items in roles_p_2.items():
        roles_p_2[role]['i_from_neutral'] = optimal_i(Rnt, Ut, roles_p_2[role]['a'], roles_p_2[role]['b'])
        roles_p_2[role]['i_bank_rate_annual'] = 3.25 + roles_p_2[role]['i_from_neutral']
        roles_p_2[role]['i_t'] = It*4 + 3.25
        roles_p_2[role]['U0'] = Ut*4
        roles_p_2[role]['Rn0'] = Rnt*4
    
    roles_to_csv(roles_p_2, f"optimal_i_for_roles_p=.2_i={POLICY_RATE}.csv")    
        
    
    #part 3.4
    roles_p_3 = find_optimal_a_b_all_roles(roles, Ut, Rnt, p=.3, save_to_csv=False, csv_name="roles_a_b_p=.3.csv")
    for role, items in roles_p_3.items():
        roles_p_3[role]['i_from_neutral'] = optimal_i(Rnt, Ut, roles_p_2[role]['a'], roles_p_2[role]['b'])
        roles_p_3[role]['i_bank_rate_annual'] = 3.25 + roles_p_3[role]['i_from_neutral']
        roles_p_3[role]['i_t'] = It*4 + 3.25
        roles_p_3[role]['U0'] = Ut*4
        roles_p_3[role]['Rn0'] = Rnt*4
        
    roles_to_csv(roles_p_2, f"optimal_i_for_roles_p=.3_i={POLICY_RATE}.csv")