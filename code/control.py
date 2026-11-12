"""Control versus consumption. Outcome (x, k): human resource share x, human control share k.
u_H = (1-c) v(x) + c k, v = 1 - exp(-s x). Pre-AI baseline: x-equivalent 1 (s=1) and full control.
AI goal is satiable: g(y) = (1 - exp(-m y)) / (1 - exp(-m)) on its resource share y = 1 - x.
Human control is used to correct the AI with probability rho * k, so AI goal value G = (1 - rho k) g(1 - x).
Control is valued by the AI only instrumentally, via correction. U_A = (1-alpha) G + alpha u_H.
d_H = (1-delta) b_H, d_A = b_A = U_A(0, 0). Asymmetric Nash with AI weight p."""
import numpy as np
X = np.linspace(0, 1, 201)[:, None]; K = np.linspace(0, 1, 201)[None, :]
def solve(alpha, c, rho, s=20, m=5, delta=0.8, p=0.5):
    v = 1 - np.exp(-s * X); uH = (1 - c) * v + c * K
    g = (1 - np.exp(-m * (1 - X))) / (1 - np.exp(-m)); G = (1 - rho * K) * g
    UA = (1 - alpha) * G + alpha * uH
    bH = (1 - c) * (1 - np.exp(-1)) + c; dH = (1 - delta) * bH; bA = UA[0, 0]
    gh, ga = uH - dH, UA - bA; ok = (gh >= 0) & (ga >= 0)
    if not ok.any(): return None
    if p >= 1: obj = np.where(ok, UA, -np.inf)
    else: obj = np.where(ok & (gh > 0) & (ga > 0), (1 - p) * np.log(np.maximum(gh, 1e-300)) + p * np.log(np.maximum(ga, 1e-300)), -np.inf)
    if not np.isfinite(obj).any(): obj = np.where(ok, UA, -np.inf)
    i = np.unravel_index(np.argmax(obj), obj.shape)
    return dict(x=float(X[i[0], 0]), k=float(K[0, i[1]]), uH=float(uH[i]), bH=float(bH), mutual=bool(uH[i] > bH + 1e-9 and UA[i] > bA + 1e-9))
def astar(**kw):
    f = lambda a: (r := solve(a, **kw)) is not None and r["mutual"]
    if f(0): return 0.0
    if not f(0.9999): return np.nan
    lo, hi = 0.0, 0.9999
    for _ in range(14):
        mid = (lo + hi) / 2; lo, hi = (lo, mid) if f(mid) else (mid, hi)
    return hi
if __name__ == "__main__":
    import json
    ce = np.exp(-1) / (1 + np.exp(-1)); print("critical c = %.3f" % ce)
    rows = []
    for c in (0.1, 0.2, 0.3, 0.5, 0.7, 0.9):
        for rho in (0.1, 0.3, 0.6, 0.9):
            for p in (0.5, 1.0):
                a = astar(c=c, rho=rho, p=p); rows.append(dict(c=c, rho=rho, p=p, astar=a, pred=rho / (rho + c) if c > ce else 0.0))
    for r in rows: print("c=%.1f rho=%.1f p=%.1f  alpha*=%.3f  rho/(rho+c)=%.3f" % (r["c"], r["rho"], r["p"], r["astar"], r["pred"]))
    json.dump(rows, open("../results/control_results.json", "w"), indent=1)
