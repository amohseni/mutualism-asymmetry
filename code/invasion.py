"""Replicator dynamics over AI variants (aligned vs misaligned) with sanctions run by AI monitors."""
import numpy as np
from sweep import solve
K = dict(kappa=100, theta=1.0, delta=1.0, p=1.0, xbar=0.05, s=3, w=0, norm=False)
xH = solve(0.995, **K)["x"]; xL = solve(0.5, **K)["x"]
print("human share kept by aligned variant %.3f, by misaligned %.3f" % (xH, xL))
def fitness_gap(z, sq0, monitors_from_population=True):
    q = sq0 * ((1 - z) if monitors_from_population else 1.0)   # misaligned monitors do not report
    return (1 - xL) * (1 - q) - (1 - xH)                      # f_L - f_H (resources kept after sanction)
def run(z0, sq0, mp=True, T=4000, dt=0.05):
    z = z0
    for _ in range(T): z += dt * z * (1 - z) * fitness_gap(z, sq0, mp)
    return z
for sq0 in [0.4, 0.7, 0.9]:
    zd = 1 - xH / sq0 if sq0 > xH else None
    print(f"sigma*q0={sq0}: tipping point z+ = {zd if zd is None else round(zd,3)};",
          "final z from z0=0.01,0.2,0.4,0.6:", [round(run(z0, sq0), 3) for z0 in (0.01, 0.2, 0.4, 0.6)],
          "| independent monitors:", [round(run(z0, sq0, False), 3) for z0 in (0.01, 0.6)])
