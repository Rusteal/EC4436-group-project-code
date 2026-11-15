# EC4436 — Deriving the period loss under a shock-based policy rule

## 1. Model and objective

Following Section 3.3 of the group-project brief, the New Keynesian model is

$$
x_t = \mathbb{E}_t[x_{t+1}] - \frac{1}{\sigma}\left(i_t-\mathbb{E}_t[\pi_{t+1}]-r_t^n\right),
\tag{1}
$$

$$
\pi_t = \beta\mathbb{E}_t[\pi_{t+1}]+\kappa x_t+u_t.
\tag{2}
$$

The proposed monetary policy rule is

$$
i_t=a u_t+b r_t^n.
\tag{3}
$$

The loss in period $t$ and total loss over $T$ quarters are, respectively,

$$
L_t=\pi_t^2+\lambda x_t^2, \qquad L=\sum_{t=1}^{T}L_t.
\tag{4}
$$

Here $u_t$ is the cost-push shock, $r_t^n$ the natural-rate (demand) shock, $a$ and $b$ the coefficients chosen by the committee, and $\lambda$ its relative weight on output-gap stabilisation. All interest rates and inflation variables are in the *per-quarter deviations* specified by the brief; the output gap is in percent.

## 2. Substitute the policy rule into the IS curve

Starting from (1), use (3):

$$
x_t=\mathbb{E}_t[x_{t+1}]-\frac{1}{\sigma}\left(a u_t+b r_t^n-\mathbb{E}_t[\pi_{t+1}]-r_t^n\right).
$$

Collect the natural-rate shock terms:

$$
x_t=\mathbb{E}_t[x_{t+1}]-\frac{1}{\sigma}\left(a u_t+(b-1)r_t^n-\mathbb{E}_t[\pi_{t+1}]\right).
$$

Hence

$$
\boxed{x_t=\mathbb{E}_t[x_{t+1}]+\frac{\mathbb{E}_t[\pi_{t+1}]+(1-b)r_t^n-a u_t}{\sigma}.}
\tag{5}
$$

For convenient notation, define the right-hand side of (5) by

$$
Q_t\equiv \mathbb{E}_t[x_{t+1}]+\frac{\mathbb{E}_t[\pi_{t+1}]+(1-b)r_t^n-a u_t}{\sigma}.
\tag{6}
$$

Then $x_t=Q_t$.

## 3. Substitute the output gap into the Phillips curve

From (2) and (6),

$$
\pi_t=\beta\mathbb{E}_t[\pi_{t+1}]+\kappa Q_t+u_t.
\tag{7}
$$

Expanding $Q_t$ gives an expression involving only next-quarter expectations, current shocks, and known coefficients:

$$
\begin{aligned}
\pi_t
&=\beta\mathbb{E}_t[\pi_{t+1}]
 +\kappa\mathbb{E}_t[x_{t+1}]
 +\frac{\kappa}{\sigma}\mathbb{E}_t[\pi_{t+1}]
 +\frac{\kappa(1-b)}{\sigma}r_t^n
 -\frac{\kappa a}{\sigma}u_t+u_t\\[2mm]
&=\left(\beta+\frac{\kappa}{\sigma}\right)\mathbb{E}_t[\pi_{t+1}]
 +\kappa\mathbb{E}_t[x_{t+1}]
 +\left(1-\frac{\kappa a}{\sigma}\right)u_t
 +\frac{\kappa(1-b)}{\sigma}r_t^n.
\end{aligned}
$$

Thus

$$
\boxed{\pi_t=\left(\beta+\frac{\kappa}{\sigma}\right)\mathbb{E}_t[\pi_{t+1}]
 +\kappa\mathbb{E}_t[x_{t+1}]
 +\left(1-\frac{\kappa a}{\sigma}\right)u_t
 +\frac{\kappa(1-b)}{\sigma}r_t^n.}
\tag{8}
$$

## 4. Explicit loss expression

Substitute (5) and (8) into $L_t=\pi_t^2+\lambda x_t^2$:

$$
\boxed{\begin{aligned}
L_t(a,b;\lambda)={}&\Bigg[
\left(\beta+\frac{\kappa}{\sigma}\right)\mathbb{E}_t[\pi_{t+1}]
+\kappa\mathbb{E}_t[x_{t+1}]
+\left(1-\frac{\kappa a}{\sigma}\right)u_t
+\frac{\kappa(1-b)}{\sigma}r_t^n
\Bigg]^2\\[2mm]
&+\lambda\Bigg[
\mathbb{E}_t[x_{t+1}]
+\frac{\mathbb{E}_t[\pi_{t+1}]}{\sigma}
-\frac{a}{\sigma}u_t
+\frac{1-b}{\sigma}r_t^n
\Bigg]^2.
\end{aligned}}
\tag{9}
$$

**Equation (9) is the requested formula:** the contemporaneous policy rate $i_t$, inflation $\pi_t$ and output gap $x_t$ have all been eliminated from the right-hand side. The only *time-varying inputs* are the current shocks and conditional expectations of next quarter's endogenous variables. Importantly, those future expectations themselves depend on $a$ and $b$ through the same model, so (9) is a **recursive expression**, not an independently evaluable closed-form function of $a,b$ without solving the subsequent periods.

For the given $\sigma=1$, equation (9) simplifies to

$$
\boxed{\begin{aligned}
L_t(a,b;\lambda)={}&\left[(\beta+\kappa)\mathbb{E}_t[\pi_{t+1}]+\kappa\mathbb{E}_t[x_{t+1}]+(1-\kappa a)u_t+\kappa(1-b)r_t^n\right]^2\\
&+\lambda\left[\mathbb{E}_t[x_{t+1}]+\mathbb{E}_t[\pi_{t+1}]-a u_t+(1-b)r_t^n\right]^2.
\end{aligned}}
\tag{10}
$$

## 5. Evaluating the loss by backward induction

The brief sets $T=20$ and terminal conditions $x_{T+1}=\pi_{T+1}=0$. Its shocks are AR(1):

$$
u_t=\rho u_{t-1}+\varepsilon_{u,t},\qquad r_t^n=\rho r_{t-1}^n+\varepsilon_{r,t},\qquad \mathbb E_t[\varepsilon_{\cdot,t+1}]=0.
$$

Conditional on the two initially identified shocks and assuming no *subsequent realised innovations* along the forecast path, use

$$
u_t=\rho^{t-1}u_1,\qquad r_t^n=\rho^{t-1}r_1^n,\qquad t=1,\ldots,T.
\tag{11}
$$

For this deterministic conditional forecast, $\mathbb{E}_t[x_{t+1}]=x_{t+1}$ and $\mathbb{E}_t[\pi_{t+1}]=\pi_{t+1}$ on the model forecast path. For each pair $(a,b)$:

1. Set $x_{T+1}=\pi_{T+1}=0$.
2. For $t=T,T-1,\ldots,1$, compute the shock values from (11), then $x_t$ from (5), then $\pi_t$ from (7), and finally $L_t$ from (4) or (9).
3. Sum $L=\sum_{t=1}^T L_t$.
4. Repeat for every specified pair of $a$ and $b$, separately for each mandate $\lambda$.

The brief's grid is $a\in\{0,0.5,1,1.5,2,3\}$ and $b\in\{0,0.5,1,1.5\}$ (24 combinations); the mandate weights are $\lambda\in\{0.05,0.25,1.00\}$, plus $0.10$ for groups of four. Experiments 1 and 2 first isolate the demand and cost-push shocks, respectively.

A compact Python implementation of the model evaluation is:

```python
import numpy as np

def evaluate_rule(a, b, lam, u1, rn1, T=20, beta=0.99,
                  sigma=1.0, kappa=0.13, rho=0.20):
    x = np.zeros(T + 2)   # indices 1,...,T+1
    pi = np.zeros(T + 2)
    loss_t = np.zeros(T + 2)

    for t in range(T, 0, -1):
        u = rho ** (t - 1) * u1
        rn = rho ** (t - 1) * rn1
        x[t] = x[t+1] + (pi[t+1] + (1-b)*rn - a*u) / sigma
        pi[t] = beta*pi[t+1] + kappa*x[t] + u
        loss_t[t] = pi[t]**2 + lam*x[t]**2

    return {
        'total_loss': loss_t[1:T+1].sum(),
        'x': x[1:T+1], 'pi': pi[1:T+1],
        'loss_by_quarter': loss_t[1:T+1],
        'policy_deviation': np.array([
            a*rho**(t-1)*u1 + b*rho**(t-1)*rn1
            for t in range(1, T+1)
        ])
    }
```

**Model interpretation:** In Experiment 1 ($u_1=0$), setting $b=1$ perfectly offsets the natural-rate shock, producing $x_t=\pi_t=0$ and zero loss. In Experiment 2 ($r_1^n=0$), the Phillips curve contains the direct cost-push term $u_t$, so the central bank cannot generally keep both inflation and the output gap at zero; the preferred $a$ depends on $\lambda$.

*Source: EC4436 Group Project brief, Part 3, Sections 3.1–3.3 (pp. 3–5).*
