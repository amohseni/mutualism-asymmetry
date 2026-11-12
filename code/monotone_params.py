"""Theorem 1 check: agreed human share x* is nonincreasing in theta, delta, p (fixed alpha), so alpha* is nondecreasing."""
import sys, numpy as np
from scipy.stats import qmc
from sweep import back, solve, astar, PARAMS
U = qmc.Sobol(d=len(PARAMS), scramble=True, seed=99).random(256)
grid = {"theta": np.linspace(0, 1, 21), "delta": np.linspace(0, 0.95, 20), "p": np.linspace(0.01, 0.99, 20)}
viol = {k: 0 for k in grid}; avio = {k: 0 for k in grid}; n = 0
for norm in (False, True):
    for u in U:
        k = back(u); k["norm"] = norm; n += 1
        al = float(np.random.default_rng(n).uniform(0, 1))
        for name, vals in grid.items():
            xs = []
            for v in vals:
                r = solve(al, **{**k, name: v}); xs.append(np.nan if r is None else r["x"])
            xs = np.array(xs); f = xs[~np.isnan(xs)]
            if (np.diff(f) > 1e-9).any(): viol[name] += 1
        if n % 8 == 0:
            for name, vals in grid.items():
                a = np.array([astar(**{**k, name: v}) for v in vals[::4]]); a = np.where(np.isnan(a), 1, a)
                if (np.diff(a) < -2e-4).any(): avio[name] += 1
print("points:", n, "| x* increases (violations):", viol, "| alpha* decreases (violations, every 8th point):", avio)
