"""
Parameter Symbol Value
Discount factor 𝛽 0.99
Inverse intertemporal elasticity of substitution 𝜎 1.0
Slope of the Phillips curve 𝜅 0.13
Shock persistence 𝜌 0.20
Horizon (quarters) 𝑇 20

Part 3 of the brief, in its order:
3.1 data to model units, 3.2 identify the shocks (reported x4 in annual terms),
3.3 Experiments 1, 2 and 3, 3.4(a) re-run at rho = 0.3.
Run with:  python3 part3_experiments.py
"""

BETA = .99
SIGMA = 1
K = .13
P = .2
T = 20

# data, annual %, only what was published on or before 5 Nov 2026 (lecturer's instruction)
CPI_YOY = 3.17          # ONS D7G7, average of Jul 2.9, Aug 3.1, Sep 3.5
E_CPI = 2.5             # Sept MaPS Q2a, "One year ahead" median (the row Appendix A names)
GAP = -1.1              # OBR Oct 2026 EFO, 2026 Q3; July MPR Table 3.B also -1.1
BANK_RATE = 3.75        # 2026 Q3, fixed by the lecturer's instruction
GDP_GROWTH = 1.1        # Sept MaPS Q2c, 2027 GDP growth median
GDP_POTENTIAL = 1.4     # Sept MaPS Q2c, "Long run (potential)" median
NEUTRAL = 3.25          # Sept MaPS Q1bi median, neutral NOMINAL Bank Rate
R_STAR = NEUTRAL - 2    # neutral REAL rate, 1.25

# 3.1 model units: per quarter, deviation from the long-run average
PIt = (CPI_YOY - 2)/4
E_PIt1 = (E_CPI - 2)/4
gap = GAP                                       # table says no conversion
E_gap = GAP + (GDP_GROWTH - GDP_POTENTIAL)/4    # Appendix A: E[x_t+1] = x_t + (g - g_pot)/4
It = BANK_RATE/4 - R_STAR/4 - 0.5               # deviation from neutral, r*/4 + 0.5


# 3.2 identify the shocks (quarterly, model units)
def identify_cost_push_shock_q(PIt, E_PIt1, Xt, beta=BETA, k=K) -> float:
    return PIt - beta*E_PIt1 - k*Xt


def identify_demand_shock_q(It, E_PIt1, Xt, E_Xt1, sigma=SIGMA) -> float:
    return It - E_PIt1 + sigma*(Xt - E_Xt1)


U1 = identify_cost_push_shock_q(PIt, E_PIt1, gap)
Rn1 = identify_demand_shock_q(It, E_PIt1, gap, E_gap)


# the model
def shock_path(U1: float, Rn1: float, p: float = P) -> tuple[list, list]:
    """u_t and rn_t for t = 1..T: the identified value in period 1, then p times the previous quarter"""
    U = [U1 * p**(t - 1) for t in range(1, T + 1)]
    Rn = [Rn1 * p**(t - 1) for t in range(1, T + 1)]
    return U, Rn


def simulate(a: float, b: float, U1: float, Rn1: float, p: float = P) -> tuple[list, list]:
    """idea: start in period T+1, where inflation and gap are 0, go back in time.
    With the rule i_t = a*u_t + b*rn_t put into the IS curve:
        x_t  = x_t+1 + (pi_t+1 + (1-b)*rn_t - a*u_t)/sigma
        pi_t = beta*pi_t+1 + k*x_t + u_t
    returns the inflation path and the output gap path for t = 1..T"""
    U, Rn = shock_path(U1, Rn1, p)
    Pi_T1, x_T1 = 0, 0                  # period T+1
    inflation_path = [0]*T
    output_gap_path = [0]*T
    for t in range(T - 1, -1, -1):      # list index T-1 is period T, index 0 is period 1
        xt = x_T1 + (Pi_T1 + (1 - b)*Rn[t] - a*U[t])/SIGMA
        pit = BETA*Pi_T1 + K*xt + U[t]
        inflation_path[t] = pit
        output_gap_path[t] = xt
        Pi_T1, x_T1 = pit, xt
    return inflation_path, output_gap_path


def loss(L: float, inflation_path: list, output_gap_path: list) -> float:
    """sum over t = 1..T of (pi_t^2 + L*x_t^2), L is the lambda of a committee member"""
    return sum(pit**2 + L*xt**2 for pit, xt in zip(inflation_path, output_gap_path))


roles: dict = {
    'hawk': 0.05,
    'hawkish centrist': .1,
    'balanced': .25,
    'dove': 1}

A_GRID = [0, 0.5, 1, 1.5, 2, 3]     # response to the cost-push shock
B_GRID = [0, 0.5, 1, 1.5]           # response to the demand shock


def experiment(coef_name: str, grid: list, a_or_b: str, U1: float, Rn1: float) -> None:
    """Experiments 1 and 2: one unit shock, vary one coefficient, record x_1, pi_1 and every member's loss"""
    print(f"{coef_name:>4}{'x_1':>9}{'pi_1':>9}" + "".join(f"{name:>18}" for name in roles))
    best = {name: (None, float("inf")) for name in roles}
    for c in grid:
        a, b = (c, 0) if a_or_b == "a" else (0, c)
        pi_path, x_path = simulate(a, b, U1, Rn1)
        row = f"{c:>4}{x_path[0]:>9.4f}{pi_path[0]:>9.4f}"
        for name, L in roles.items():
            l = loss(L, pi_path, x_path)
            row += f"{l:>18.5f}"
            if l < best[name][1]:
                best[name] = (c, l)
        print(row)
    print("best " + coef_name + ": " + ", ".join(f"{name} {best[name][0]}" for name in roles))


def experiment_3(U1: float, Rn1: float, p: float = P, show_grid: str = 'hawk') -> None:
    """Experiment 3: both shocks at identified values, 24 cells, each member's optimum as a rate decision"""
    L = roles[show_grid]
    print(f"loss grid for the {show_grid} (lambda = {L}), rows a, columns b")
    print("       " + "".join(f"{'b=' + str(b):>10}" for b in B_GRID))
    for a in A_GRID:
        print(f"a={a:<5}" + "".join(f"{loss(L, *simulate(a, b, U1, Rn1, p)):>10.4f}" for b in B_GRID))

    print(f"\n{'member':<18}{'a':>5}{'b':>5}{'loss':>10}{'i_1':>9}{'annual rate':>13}{'change':>9}")
    for name, L in roles.items():
        cells = {(a, b): loss(L, *simulate(a, b, U1, Rn1, p)) for a in A_GRID for b in B_GRID}
        a, b = min(cells, key=cells.get)
        i1 = a*U1 + b*Rn1                       # model units, deviation from neutral
        rate = 4*i1 + (R_STAR + 2)              # back to an annual Bank Rate
        change = round((rate - BANK_RATE)*100)  # basis points against 3.75
        print(f"{name:<18}{a:>5}{b:>5}{cells[(a, b)]:>10.4f}{i1:>9.4f}{rate:>12.2f}%{change:>+7d}bp")


if __name__ == "__main__":
    print("3.1 MODEL UNITS (per quarter, deviation from long-run average)")
    print(f"  pi_t = {PIt:+.4f}   E[pi_t+1] = {E_PIt1:+.4f}")
    print(f"  x_t  = {gap:+.4f}   E[x_t+1]  = {E_gap:+.4f}")
    print(f"  i_t  = {It:+.4f}   (r* = {R_STAR:.2f})")

    print("\n3.2 IDENTIFIED SHOCKS")
    print(f"  cost-push u_1 = {U1:+.4f} per quarter = {4*U1:+.2f} pp of annual inflation")
    print(f"  demand   rn_1 = {Rn1:+.4f} per quarter = {4*Rn1:+.2f} pp of the annual natural rate")

    print("\nEXPERIMENT 1: demand shock alone (rn_1 = 1, u = 0, a = 0), vary b")
    experiment("b", B_GRID, "b", U1=0, Rn1=1)

    print("\nEXPERIMENT 2: cost-push shock alone (u_1 = 1, rn = 0, b = 0), vary a")
    experiment("a", A_GRID, "a", U1=1, Rn1=0)

    print("\nEXPERIMENT 3: both shocks at identified values, rho = 0.2")
    experiment_3(U1, Rn1)

    print("\n3.4(a) RE-RUN AT rho = 0.3")
    print("  shocks: the identification uses the survey's expectations directly and rho does not")
    print(f"  enter it, so u_1 = {4*U1:+.2f} pp and rn_1 = {4*Rn1:+.2f} pp annual, unchanged")
    experiment_3(U1, Rn1, p=0.3)
