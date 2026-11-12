"""Data for Figures 1 and 2 of the paper (illustrative path; exchange threshold)."""
import sys, csv, numpy as np
from model import solve, mutual, astar, traj
bH = 1 - np.exp(-1)
base = dict(xbar=0.05, s=3, w=0, norm=False, bH=bH)
out = "../paper/data/"
# Figure 1: the illustrative path
rows = []
for t in np.round(np.linspace(0, 1, 201), 4):
    k = dict(traj(t), **base)
    x, uH, uA, bA, _, _ = solve(0.0, **k)
    a = astar(mutual, **k)
    dH = (1-k['delta'])*bH
    rows.append(dict(t=t, uH=uH if uH >= 0 else dH, dH=dH, bH=bH, alpha_star=a))
with open(out + 'path.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
# Figure 2: human payoff at agreement against independence, for three bargaining powers
rows = []
for p in [0.15, 0.5, 0.85]:
    for th in np.round(np.linspace(0, 1, 201), 4):
        for kap in [1, 1000]:
            x, uH, *_ = solve(0.0, kappa=kap, theta=th, delta=0.5, p=p, **base)
            dH = 0.5*bH
            best = 1-np.exp(-3*(1-th)) if 1-th >= base['xbar'] else np.nan
            rows.append(dict(p=p, theta=th, kappa=kap, uH=uH if uH >= 0 else dH, best=best, dH=dH))
with open(out + 'exchange.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
