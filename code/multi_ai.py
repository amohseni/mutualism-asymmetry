"""Several AIs. (a) Competition for human cooperation: n >= 2 AIs bid for one human partner; partner productivity kappa,
non-partner kappa*theta. Bertrand: human share x = 1 - theta (for alpha = 0).
(b) Care as a public good: AI i holds share r_i, gives x_i, payoff (1-alpha_i) kappa (r_i - x_i) + alpha_i v(X), X = sum x_i.
Nash equilibrium (Bergstrom, Blume and Varian 1986): only the most caring AIs give; X = max_k min(Xbar_k, sum_{j<=k} r_j)
with AIs sorted by their ideal level Xbar_i solving alpha_i v'(Xbar) = (1-alpha_i) kappa.
Dynamics: next-period shares proportional to kept resources r_i - x_i."""
import numpy as np, json
s, kappa = 3.0, 100.0
v = lambda x: 1 - np.exp(-s * x); xh = 1 / s  # v(xh) = b_H = 1 - e^-1
def ideal(a):
    if a <= 0: return 0.0
    return max(0.0, np.log(s * a / ((1 - a) * kappa)) / s) if a < 1 else 1.0
def equilibrium(r, al):
    """Most caring give first; AIs with equal ideal levels split the burden in proportion to their shares."""
    x = np.zeros(len(r)); X = 0.0
    for lvl in sorted({ideal(a) for a in al}, reverse=True):
        grp = [i for i in range(len(r)) if ideal(al[i]) == lvl]
        need = max(0.0, lvl - X); cap = sum(r[i] for i in grp)
        if cap > 0 and need > 0:
            f = min(1.0, need / cap)
            for i in grp: x[i] = f * r[i]
            X += f * cap
    return x, X
def run(r0, al, T=60, gamma=0.1):
    """Each period world output is 1, split by capital shares r_i; capital grows by gamma times kept output."""
    R = np.array(r0, float); out = []
    for t in range(T):
        r = R / R.sum(); x, X = equilibrium(r, al)
        out.append(dict(t=t, shares=r.round(3).tolist(), X=round(X, 3), mutual=bool(X > xh)))
        R = R + gamma * (r - x)
    return out
if __name__ == "__main__":
    print("Bertrand human share 1 - theta:", {th: round(1 - th, 2) for th in (0.1, 0.5, 0.9, 1.0)})
    print("x_h = %.3f; ideal X for alpha 0.995: %.3f, 0.999: %.3f, 0.5: %.3f" % (xh, ideal(0.995), ideal(0.999), ideal(0.5)))
    res = {}
    for name, r0, al in [("one caring AI of three, equal shares", [1/3, 1/3, 1/3], [0.995, 0.5, 0.0]),
                         ("one caring AI holding 0.8", [0.8, 0.1, 0.1], [0.995, 0.5, 0.0]),
                         ("one caring AI holding 0.95, alpha 0.999", [0.95, 0.05], [0.999, 0.0]),
                         ("all caring alike", [0.5, 0.5], [0.995, 0.995])]:
        tr = run(r0, al); res[name] = tr
        print(name); [print("  t=%d shares=%s X=%.3f mutual=%s" % (q["t"], q["shares"], q["X"], q["mutual"])) for q in tr[::10]]
        fail = next((q["t"] for q in tr if not q["mutual"]), None); print("  first period without mutualism:", fail)
    json.dump(res, open("../results/multi_ai_results.json", "w"), indent=1)
