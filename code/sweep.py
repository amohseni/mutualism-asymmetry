"""Sobol sweep of the base mutualism model (stage 3). Deterministic model, one run per point."""
import numpy as np, json, sys, hashlib
from multiprocessing import Pool
from scipy.stats import qmc

X = np.linspace(0, 1, 2001)
BH = 1 - np.exp(-1)            # pre-AI human baseline (all resources, slope 1)

# name, low, high, scale
PARAMS = [("kappa", 1, 1e4, "log"), ("theta", 0, 1, "lin"), ("delta", 0, 1, "lin"),
          ("p", 0, 1, "lin"), ("xbar", 0.01, 0.3, "log"), ("s", 1.5, 100, "log"), ("w", 0, 1, "lin")]

def back(u):
    out = {}
    for (n, lo, hi, sc), v in zip(PARAMS, u):
        out[n] = float(np.exp(np.log(lo) + v * (np.log(hi) - np.log(lo)))) if sc == "log" else float(lo + v * (hi - lo))
    return out

def solve(alpha, kappa, theta, delta, p, xbar, s, w, norm):
    m = (X >= xbar).astype(float)
    G = (1 - X) * (theta + (1 - theta) * m)
    if not norm: G = kappa * G
    v = w * X + (1 - w) * (1 - np.exp(-s * X))
    UA = (1 - alpha) * G + alpha * v
    bA = UA[0]; dH = (1 - delta) * BH
    ok = (v >= dH) & (UA >= bA)
    if not ok.any(): return None
    gh = np.clip(v - dH, 0, None); ga = np.clip(UA - bA, 0, None)
    if p >= 1 - 1e-9:
        idx = np.where(ok)[0]; i = idx[np.argmax(UA[idx])]
    elif p <= 1e-9:
        idx = np.where(ok)[0]; i = idx[np.argmax(v[idx])]
    else:
        with np.errstate(divide="ignore"):
            obj = (1 - p) * np.log(gh) + p * np.log(ga)
        obj[~ok] = -np.inf
        i = int(np.argmax(obj))
        if not np.isfinite(obj[i]): return None
    return dict(x=X[i], uH=v[i], UA=UA[i], bA=bA, ex=(1 - alpha) * (G[i] - G[0]))

def mutual(alpha, **k):
    r = solve(alpha, **k)
    return bool(r is not None and r["uH"] > BH + 1e-9 and r["UA"] > r["bA"] + 1e-9)

def exchange(**k):
    r = solve(0.0, **k)
    return r is not None and r["uH"] > BH + 1e-9 and r["ex"] > 1e-9

def astar(**k):
    if mutual(0.0, **k): return 0.0
    if not mutual(0.9999, **k): return float("nan")
    lo, hi = 0.0, 0.9999
    for _ in range(16):
        mid = (lo + hi) / 2
        if mutual(mid, **k): hi = mid
        else: lo = mid
    return hi

def run(args):
    u, norm = args
    k = back(u); k["norm"] = norm
    r0 = solve(0.0, **k)
    return dict(**{n: k[n] for n, *_ in PARAMS}, norm=norm, astar=astar(**k), exchange=bool(exchange(**k)),
                agree0=bool(r0 is not None), uH0=None if r0 is None else float(r0["uH"]), x0=None if r0 is None else float(r0["x"]))

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16384
    U = qmc.Sobol(d=len(PARAMS), scramble=True, seed=20261012).random(n)
    jobs = [(u, norm) for norm in (False, True) for u in U]
    with Pool(4) as pool: rows = pool.map(run, jobs, chunksize=64)
    code_hash = hashlib.sha256(open(__file__, "rb").read()).hexdigest()[:12]
    json.dump(dict(seed=20261012, n=n, code_hash=code_hash, numpy=np.__version__, rows=rows), open("../results/sweep_manifest.json", "w"))
    print("done", len(rows), code_hash)
