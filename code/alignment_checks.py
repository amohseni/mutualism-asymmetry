"""Checks cited in the text of Sections 4 and 5.2.
(1) Where exchange mutualism ends on the illustrative path, and with bargaining power held fixed.
(2) Proposition 4: the solution-free bound alpha* >= kappa x_h / (kappa x_h + b_H) and the p -> 1 value."""
import numpy as np
from sweep import mutual, astar
BASE = dict(xbar=0.05, s=3, w=0, norm=False)
def traj(t, p=None):
    return dict(kappa=10 ** (3 * t), theta=0.1 + 0.9 * t, delta=0.2 + 0.75 * t, p=min(0.999, 0.15 + 0.85 * t ** 0.5) if p is None else p)
ts = np.round(np.linspace(0, 1, 201), 3)
for p in (None, 0.15, 0.5):
    t = next(t for t in ts if not mutual(0.0, **traj(t, p), **BASE))
    print("exchange mutualism ends at t = %.3f (theta = %.3f), p = %s" % (t, 0.1 + 0.9 * t, "path" if p is None else p))
print("dependence bound theta = 1 - x_h = 2/3 is reached at t = %.3f" % ((2 / 3 - 0.1) / 0.9))
kappa, xh, bH = 10.0, 1 / 3, 1 - np.exp(-1)
print("Prop 4 at kappa = 10, s = 3: bound (i) %.4f, value (ii) %.4f" % (kappa * xh / (kappa * xh + bH), kappa / (kappa + 3 * np.exp(-1))))
for p in (0.1, 0.5, 0.9, 0.999):
    print("   p = %.3f: alpha* = %.4f at delta = 0, %.4f at delta = 0.5" % (p, astar(kappa=kappa, theta=1.0, delta=0.0, p=p, **BASE), astar(kappa=kappa, theta=1.0, delta=0.5, p=p, **BASE)))
