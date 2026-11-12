import json, numpy as np
from scipy.stats import spearmanr
D = json.load(open("../results/sweep_manifest.json")); R = D["rows"]
P = ["kappa","theta","delta","p","xbar","s","w"]
def lab(a):
    if a != a: return "impossible"
    if a == 0: return "exchange"
    if a < 0.9: return "care"
    return "near-perfect care"
for norm in (False, True):
    rows=[r for r in R if r["norm"]==norm]
    A=np.array([r["astar"] for r in rows]); Ae=np.where(np.isnan(A),1.0,A)
    X=np.array([[np.log10(r[p]) if p in ("kappa","xbar","s") else r[p] for p in P] for r in rows])
    labs=[lab(a) for a in A]
    print("\n== convention:", "goal value independent of capability" if norm else "goal value scales with capability")
    for L in ["exchange","care","near-perfect care","impossible"]: print(f"  {L:18s} {labs.count(L)/len(labs):.3f}")
    print("  exchange flag share", np.mean([r["exchange"] for r in rows]))
    print("  Spearman rho of alpha* (impossible=1) with:")
    for j,p in enumerate(P): print(f"    {p:6s} {spearmanr(X[:,j],Ae)[0]:+.3f}")
    # regimes
    later=(X[:,1]>0.8)&(X[:,2]>0.7)&(X[:,3]>0.7)
    now=(X[:,1]<0.3)&(X[:,2]<0.4)&(X[:,3]<0.4)
    for name,mask in [("now-like",now),("later-like",later)]:
        sub=[labs[i] for i in np.where(mask)[0]]
        print(f"  {name} n={mask.sum()}:", {L: round(sub.count(L)/len(sub),3) for L in ["exchange","care","near-perfect care","impossible"]}, "median alpha*", round(float(np.nanmedian(A[mask])),3))
    # exchange vs theta boundary: check prop1 bound theta < 1-max(xbar,x_h)
    if not norm:
        xh=np.array([None]*len(rows))
