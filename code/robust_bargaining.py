"""Does alpha* depend on the bargaining solution? Symmetric Nash vs Kalai-Smorodinsky vs egalitarian."""
import numpy as np
from scipy.stats import qmc, spearmanr
from sweep import back, PARAMS, BH, X
def outcome(alpha, sol, kappa, theta, delta, p, xbar, s, w, norm):
    m = (X >= xbar).astype(float); G = (1 - X) * (theta + (1 - theta) * m)
    if not norm: G = kappa * G
    v = w * X + (1 - w) * (1 - np.exp(-s * X)); UA = (1 - alpha) * G + alpha * v
    bA = UA[0]; dH = (1 - delta) * BH; gh = v - dH; ga = UA - bA
    ok = (gh >= 0) & (ga >= 0)
    if not ok.any(): return None
    if sol == "nash": obj = np.where(ok, gh * ga, -1)
    elif sol == "ks":
        mh, ma = gh[ok].max(), ga[ok].max()
        obj = np.where(ok, np.minimum(gh / max(mh, 1e-12), ga / max(ma, 1e-12)), -1)
    else: obj = np.where(ok, np.minimum(gh, ga), -1)
    i = int(np.argmax(obj)); return v[i] > BH + 1e-9 and UA[i] > bA + 1e-9
def astar(sol, **k):
    if outcome(0, sol, **k): return 0.0
    if not outcome(0.9999, sol, **k): return np.nan
    lo, hi = 0.0, 0.9999
    for _ in range(14):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if outcome(mid, sol, **k) else (mid, hi)
    return hi
U = qmc.Sobol(d=len(PARAMS), scramble=True, seed=11).random(512)
res = {s: [] for s in ("nash", "ks", "egal")}
for u in U:
    k = back(u); k["norm"] = False
    for s in res: res[s].append(astar(s, **k))
A = {s: np.where(np.isnan(np.array(v)), 1, np.array(v)) for s, v in res.items()}
th = np.array([back(u)["theta"] for u in U]); kap = np.array([back(u)["kappa"] for u in U])
for s in ("ks", "egal"):
    print(s, "Spearman with Nash %.3f" % spearmanr(A["nash"], A[s])[0], "| median abs diff %.3f" % np.median(np.abs(A["nash"] - A[s])))
for s in A:
    hi = (th > 0.8)
    print(s, "share exchange %.3f" % np.mean(A[s] == 0), "| theta>0.8: median alpha* %.3f, rho with kappa %.3f" % (np.median(A[s][hi]), spearmanr(kap[hi], A[s][hi])[0]))
