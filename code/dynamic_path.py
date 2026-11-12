"""Illustrative path with selection. Along the stage 2 path (kappa, theta, delta, p rising with t), a population of AI
variants with different alignment alpha bargains with humans each generation. A variant's fitness is its goal output per unit capability,
G_i / kappa = (1 - x_i)[theta + (1 - theta) 1{x_i >= xbar}], reduced by sanctions. Monitors are AIs: only aligned variants (alpha >= 0.99) report, and evaluation
quality falls with capability, so detection q(t) = q0 * (aligned share) / (1 + kappa(t) / kappa_e).
Discrete replicator: z_i' proportional to z_i * exp(lam * (g_i - sanction_i)), with g_i = G_i / kappa in [0, 1].
lam is the speed of selection relative to the pace of the path."""
import sys, json, numpy as np
from sweep import solve, BH
ALPHAS = np.array([0.0, 0.5, 0.9, 0.99, 0.999]); Z0 = np.array([0.01, 0.04, 0.15, 0.40, 0.40])
BASE = dict(xbar=0.05, s=3, w=0, norm=False)
def traj(t): return dict(kappa=10 ** (3 * t), theta=0.1 + 0.9 * t, delta=0.2 + 0.75 * t, p=min(0.999, 0.15 + 0.85 * t ** 0.5))
def outcomes(t):
    xs, us = [], []
    for a in ALPHAS:
        r = solve(a, **traj(t), **BASE)
        x, u = (0.0, (1 - traj(t)["delta"]) * BH) if r is None else (r["x"], r["uH"])
        xs.append(x); us.append(u)
    return np.array(xs), np.array(us)
def run(T=200, lam=0.5, sigma=0.5, q0=0.9, kappa_e=10.0, select=True):
    z = Z0.copy(); rows = []
    for g in range(T + 1):
        t = g / T; x, u = outcomes(t)
        aligned = z[ALPHAS >= 0.99].sum(); q = q0 * aligned / (1 + traj(t)["kappa"] / kappa_e)
        sanc = np.where(ALPHAS >= 0.99, 0.0, sigma * q)
        th = traj(t)["theta"]; f = (1 - x) * (th + (1 - th) * (x >= BASE["xbar"])) - sanc
        rows.append(dict(t=round(t, 3), mean_alpha=float(z @ ALPHAS), aligned=float(aligned), uH=float(z @ u), mutual=bool(z @ u > BH + 1e-9), q=float(q), z=z.round(4).tolist()))
        if select:
            w = z * np.exp(lam * f); z = w / w.sum()
    return rows
if __name__ == "__main__":
    out = {}
    for name, kw in [("fixed", dict(select=False)), ("slow selection (lam 0.02)", dict(lam=0.02)), ("medium selection (lam 0.1)", dict(lam=0.1)), ("fast selection (lam 0.5)", dict(lam=0.5)),
                     ("medium, no capability blindness", dict(lam=0.1, kappa_e=1e12)), ("medium, no sanctions", dict(lam=0.1, sigma=0.0))]:
        rows = run(**kw); out[name] = rows
        fail = next((r["t"] for r in rows if not r["mutual"] and r["t"] > 0.05), None)
        print("%-36s first t without mutualism: %s" % (name, fail))
        for r in rows[::25]: print("   t=%.3f mean alpha=%.3f aligned=%.3f uH=%.3f q=%.3f" % (r["t"], r["mean_alpha"], r["aligned"], r["uH"], r["q"]))
    print("b_H = %.3f" % BH)
    json.dump(out, open("../results/dynamic_path.json", "w"))
    import csv   # data for Figure 3
    with open("../paper/data/dynamic_path.csv", "w", newline="") as f:
        wr = csv.writer(f); wr.writerow(["case", "t", "uH", "mean_alpha"])
        for case, key in [("No selection", "fixed"), ("Slow", "slow selection (lam 0.02)"), ("Medium", "medium selection (lam 0.1)"), ("Fast", "fast selection (lam 0.5)")]:
            for r in out[key]: wr.writerow([case, r["t"], r["uH"], r["mean_alpha"]])
