"""Check of Proposition 1(ii): with alpha = 0 and a cost of conflict for the AI gamma in [0, theta],
a share that the AI prefers to disagreement and that leaves humans above their baseline exists
  only if  x_h < 1 - theta + gamma,
  if       max(xbar, x_h) < 1 - theta + gamma,
and exactly when  x_h < 1 - theta + gamma  and  (xbar < 1 - theta + gamma  or  x_h < min(xbar, gamma / theta)).
Brute-force search over shares at random parameter points. Payoffs are in units of kappa."""
import numpy as np
rng = np.random.default_rng(20261112); X = np.linspace(0, 1, 20001); n = bad = 0
for _ in range(20000):
    theta = rng.uniform(0.02, 1); gamma = rng.uniform(0, theta); xbar = rng.uniform(0.01, 0.5)
    s = np.exp(rng.uniform(np.log(1.2), np.log(50))); xh = 1 / s            # u_H(x) = 1 - exp(-s x), b_H = 1 - 1/e
    G = (1 - X) * (theta + (1 - theta) * (X >= xbar))                       # goal output / kappa
    exists = bool(((G > theta - gamma) & (X > xh)).any())                   # AI prefers share to disagreement; humans above baseline
    L = 1 - theta + gamma
    exact = xh < L and (xbar < L or xh < min(xbar, gamma / theta))
    if min(abs(xh - L), abs(xbar - L), abs(xh - gamma / theta), abs(xh - xbar)) < 2e-4: continue   # skip grid-resolution ties
    n += 1
    bad += (exists != exact) or (exists and not xh < L) or (max(xbar, xh) < L and not exists)
print("points checked: %d, violations: %d" % (n, bad))
