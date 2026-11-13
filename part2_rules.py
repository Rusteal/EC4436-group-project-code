# EC4436 Part 2: three policy rules for the Bank of England.
# Formulas from the brief, Part 2. Inputs and sources are listed in README.md.
# Run with:  python3 part2_rules.py

import matplotlib.pyplot as plt


def taylor(r, pi, gap):
    return r + pi + 0.5 * (pi - 2) + 0.5 * gap


def balanced(r, pi, gap):
    return r + pi + 0.5 * (pi - 2) + 1.0 * gap


def inertial(r, pi, gap, i_prev):
    return 0.85 * i_prev + 0.15 * balanced(r, pi, gap)


# ---- Prescriptions for 2026 Q3 (annual %) ----
pi = 3.17                    # CPI inflation, average of Jul 2.9, Aug 3.1, Sep 3.5 (2026)
gap = -1.1                   # output gap, 2026 Q3
i_prev = 3.75                # Bank Rate in 2026 Q2

print("r*     Taylor  Balanced  Inertial")
for r in [1.00, 1.25, 1.50]:  # low, median, high
    print(f"{r:.2f}   {taylor(r, pi, gap):6.2f}  {balanced(r, pi, gap):8.2f}  {inertial(r, pi, gap, i_prev):8.2f}")


# ---- Question (a): the rules against what the Bank did, r* = 1.25 ----
# quarter, CPI, output gap, Bank Rate at quarter end, Bank Rate the quarter before
history = [
    ("2025 Q1", 2.80, -0.6, 4.50, 4.75),
    ("2025 Q2", 3.50, -0.7, 4.25, 4.50),
    ("2025 Q3", 3.80, -0.8, 4.00, 4.25),
    ("2025 Q4", 3.40, -0.9, 3.75, 4.00),
    ("2026 Q1", 3.10, -1.0, 3.75, 3.75),
    ("2026 Q2", 2.73, -1.1, 3.75, 3.75),
    ("2026 Q3", 3.17, -1.1, 3.75, 3.75),
]

#may change history format for proper code quality, but does not matter really
def rules_vs_historical(history, r: float = 1.25, saveplot: bool = True, showplot: bool = False) -> None:
    r = 0
    quarters, actual, tay, bal, ine = [], [], [], [], []
    print("\nquarter  Bank Rate  Taylor  Balanced  Inertial")
    for q, cpi, x, rate, prev in history:
        quarters.append(q)
        actual.append(rate)
        tay.append(taylor(r, cpi, x))
        bal.append(balanced(r, cpi, x))
        ine.append(inertial(r, cpi, x, prev))
        print(f"{q}  {rate:9.2f}  {tay[-1]:6.2f}  {bal[-1]:8.2f}  {ine[-1]:8.2f}")

    print("\nAverage distance from Bank Rate, percentage points")
    for name, rule in [("Taylor", tay), ("Balanced", bal), ("Inertial", ine)]:
        distance = sum(abs(p - a) for p, a in zip(rule, actual)) / len(actual)
        print(f"{name:9} {distance:.2f}")


    # ---- Chart ----
    plt.plot(quarters, actual, "k-o", linewidth=2.5, label="Bank Rate")
    plt.plot(quarters, tay, "-o", label="Taylor (1993)")
    plt.plot(quarters, bal, "-o", label="Balanced approach")
    plt.plot(quarters, ine, "-o", label="Inertial")
    plt.ylabel("annual %")
    plt.title(f"Policy rules against Bank Rate (r* = {r})")
    plt.legend()
    plt.grid(alpha=0.3)
    if showplot:
        plt.show()
    if saveplot:
        plt.savefig(f"part2_rules_history_r{r}.png", dpi=150)
        print(f"\nSaved part2_rules_history_r{r}.png")

if __name__ == "__main__":
    for r in [1, 1.25, 1.5]:
        rules_vs_historical(history, r)

"""Then need to answer: 
(a) which rule best describes what your central bank has been doing?
(b) which should guide the decision. 
(c) how much does 𝑟∗ matter? Report each prescription at a low
and a high 𝑟∗.

a) Here obrserve from the plot that closeset line to the observed pank policy is the inertial (.16pp avarage distance over 2025 to 2026 data, copared to .67pp and 1.03pp for Taylor and Balance respectivelly)
b) This is a phylosophical question, and answer depends on hte goals and Bank Mandate. 
Inertial approach is better for finacial stability (as rates change is smoother) but it is less ruthless then Taylor model, slower to react then both Taylor and Balanced approach
Inertial approach is (was) appropriate as there is an expectations effect, which allows for promised delayed reaction and smaller reation in the present
Bank has proven itself to be competent and accumulated a lot of credibility hence why inertial approach was used
One could agrue that Bank's primary objective is to maintain price stability therfore Taylor can be more approprite rule
Members of monetary policy commitee may have their own views on which rule is more appropriate and this will (or can) be reflected in hte minutes and their personal statements 
c) It seems that r* heavilly affect Taylor and Balanced rules, meanwhile inertial is being affected by r* but not as much (as expected as it takes only .15 of balanced), this was obvious from the rules definition

"""
