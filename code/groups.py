"""Several human groups. Elite E (population share eta) holds what the AI depends on (compute, supply chain);
the mass P does not (labor obsolete). Shares x_E, x_P; AI keeps 1 - x_E - x_P.
Per-capita utility u_j = v(x_j / pop_j), v = 1 - exp(-s y); pre-AI baseline b = 1 - e^-1 for both groups.
AI goal: G = kappa (1 - x_E - x_P) [theta + (1 - theta) 1{x_E >= xbar}]: it depends on the elite only.
Elite cares about the mass with weight beta. U_A = (1-alpha) G + alpha (eta u_E + (1-eta) u_P).
Disagreement: d_E = (1 - dE) b, d_P = (1 - dP) b, d_A = U_A at zero human shares.
Three-player asymmetric Nash with weights (pA, pE, pP)."""
import numpy as np
n = 241; g = np.linspace(0, 1, n); XE, XP = np.meshgrid(g, g, indexing="ij"); FEAS = XE + XP <= 1 + 1e-12
B = 1 - np.exp(-1)
def solve(alpha, theta, beta=0.0, net=False, eta=0.05, kappa=100, s=10, xbar=0.05, dE=0.2, dP=0.8, w=(0.5, 0.35, 0.15)):
    v = lambda y: 1 - np.exp(-s * y)
    uE0 = v(np.clip(XE - net * xbar * (XE >= xbar), 0, None) / eta); uP = v(XP / (1 - eta)); uE = (1 - beta) * uE0 + beta * uP
    G = kappa * np.clip(1 - XE - XP, 0, 1) * (theta + (1 - theta) * (XE >= xbar))
    UA = (1 - alpha) * G + alpha * (eta * uE0 + (1 - eta) * uP)
    bA = UA[0, 0]; dEv = (1 - beta) * (1 - dE) * B + beta * (1 - dP) * B; dPv = (1 - dP) * B
    ga, ge, gp = UA - bA, uE - dEv, uP - dPv
    ok = FEAS & (ga > 0) & (ge > 0) & (gp > 0)
    if not ok.any(): return None
    obj = np.where(ok, w[0] * np.log(np.where(ok, ga, 1)) + w[1] * np.log(np.where(ok, ge, 1)) + w[2] * np.log(np.where(ok, gp, 1)), -np.inf)
    i = np.unravel_index(np.argmax(obj), obj.shape)
    return dict(xE=XE[i], xP=XP[i], uE=uE0[i], uP=uP[i], avg=eta * uE0[i] + (1 - eta) * uP[i])
def astar(group, **kw):
    f = lambda a: (r := solve(a, **kw)) is not None and r[group] > B + 1e-9
    if f(0): return 0.0
    if not f(0.9999): return np.nan
    lo, hi = 0.0, 0.9999
    for _ in range(14):
        mid = (lo + hi) / 2; lo, hi = (lo, mid) if f(mid) else (mid, hi)
    return hi
if __name__ == "__main__":
    import json; rows = []
    print("Result 2 (elite uses up the input it supplies). baseline b = %.3f" % B)
    for theta in (0.1, 0.5, 0.9):
        a = {g: astar(g, theta=theta, net=True) for g in ("uE", "uP", "avg")}
        rows.append(dict(theta=theta, astar=a))
        print("theta=%.2f alpha* elite %.3f rest %.3f average %.3f" % (theta, a["uE"], a["uP"], a["avg"]))
    th = next(t for t in np.round(np.arange(0.5, 1.0, 0.01), 2) if astar("uE", theta=t, net=True) > 0)
    print("elite needs alignment first at theta = %.2f" % th)
    print("sensitivity, alpha* of the rest at theta = 0.5:")
    for lab, kw in [("paper", {}), ("rest has elite cost of conflict (dP = 0.2)", dict(dP=0.2)), ("equal human bargaining weights", dict(w=(0.5, 0.25, 0.25)))]:
        print("   %-45s %.3f" % (lab, astar("uP", theta=0.5, net=True, **kw)))
    json.dump(dict(rows=rows, elite_threshold=th), open("../results/groups_results.json", "w"), indent=1, default=float)
