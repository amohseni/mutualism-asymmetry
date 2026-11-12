"""Robustness checks, not reported in the paper: Propositions 1 and 4(ii) with nonlinear goal output phi and smooth complementarity."""
import numpy as np
X = np.linspace(0, 1, 200001)
bH = 1 - np.exp(-1)
def v(x, s): return 1 - np.exp(-s * x)
def vp(x, s): return s * np.exp(-s * x)
# Prop 3 general: phi(r) = r**e (concave), theta=1, delta=1, p=1
print("Proposition 4(ii): alpha* = k phi'(1-xh) / (k phi'(1-xh) + v'(xh))")
for k, s, e in [(5, 3, 0.5), (50, 3, 0.5), (50, 10, 0.7), (500, 4, 0.3)]:
    xh = np.log(1 / (1 - bH)) / s
    phip = e * (1 - xh) ** (e - 1)
    pred = k * phip / (k * phip + vp(xh, s))
    al = np.linspace(0, 0.99999, 200001)
    def mutual(a):
        U = (1 - a) * k * (1 - X) ** e + a * v(X, s)
        i = np.argmax(U); return v(X[i], s) > bH + 1e-12 and U[i] > U[0] + 1e-12
    lo, hi = 0.0, 0.99999
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if mutual(mid) else (mid, hi)
    print(f"  k={k} s={s} e={e}: numeric {hi:.5f}  formula {pred:.5f}")
# Prop 1 general: smooth complementarity c(x) = theta + (1-theta) min(1, x/xbar)**g, phi(r) = r**e
print("Proposition 1: exchange mutualism iff theta < Theta* = sup_{x>xh} phi(1-x) c(x)  (theta-dependent c: solve fixed point)")
for s, xbar, g, e in [(3, 0.2, 2, 1), (3, 0.5, 1, 0.6), (8, 0.1, 0.5, 1)]:
    xh = np.log(1 / (1 - bH)) / s
    def gain(th):
        c = th + (1 - th) * np.minimum(1, X / xbar) ** g
        G = (1 - X) ** e * c
        return (G[X > xh] > th + 1e-12).any()
    ths = np.linspace(0, 1, 2001); ok = np.array([gain(t) for t in ths])
    thr = ths[np.argmin(ok)] if (~ok).any() else 1
    print(f"  s={s} xbar={xbar} g={g} e={e}: exchange holds for theta < {thr:.4f}; bound phi(1-xh) = {(1-xh)**e:.4f}")
