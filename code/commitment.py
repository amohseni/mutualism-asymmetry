"""Two-period commitment model: humans decide, while they still hold power, whether to halt the transition."""
import numpy as np, json
from sweep import solve, BH
NOW = dict(kappa=2, theta=0.2, delta=0.2, p=0.2, xbar=0.05, s=3, w=0, norm=False)
r1 = solve(0.0, **NOW)
def halt_payoffs(alpha):
    r = solve(alpha, **NOW); return r["uH"], r["UA"]
def later(alpha, theta2, p2, kappa2=100, delta2=0.8, s2=10):
    return solve(alpha, kappa=kappa2, theta=theta2, delta=delta2, p=p2, xbar=0.05, s=s2, w=0, norm=False)
ALPHA_NOW = 0.3
def outcome(alpha, theta2, p2, commit=False):
    uH1, UA1 = halt_payoffs(alpha)   # one AI: same alignment in both periods (v1.1; v1.0 held period-1 alignment at ALPHA_NOW)
    X = np.linspace(0, 1, 2001)
    # efficient continuation: some later outcome beats halting for both
    G = 100 * (1 - X) * (theta2 + (1 - theta2) * (X >= 0.05)); v = 1 - np.exp(-10 * X)
    UA = (1 - alpha) * G + alpha * v
    eff = ((v >= uH1) & (UA >= UA1)).any()
    if commit:   # AI can bind itself in period 1 to any later x: humans continue if efficient
        return "continue" if eff else "halt (efficient)"
    r2 = later(alpha, theta2, p2)
    if r2 is not None and r2["uH"] >= uH1: return "continue"
    return "breakdown" if eff else "halt (efficient)"
if __name__ == "__main__":
    print("now: uH1 at alpha 0 = %.3f (bH=%.3f)" % (halt_payoffs(0.0)[0], BH))
    grid = np.linspace(0, 1, 41); res = {}
    for alpha in [0, 0.3, 0.5, 0.8, 0.9, 0.95, 0.99, 0.995, 0.998]:
        lab = [outcome(alpha, t, p) for t in grid for p in grid]
        res[alpha] = {k: round(lab.count(k) / len(lab), 3) for k in set(lab)}
        print(alpha, res[alpha])
    lab = [outcome(0, t, p, commit=True) for t in grid for p in grid]
    print("alpha 0 with commitment", {k: round(lab.count(k) / len(lab), 3) for k in set(lab)})
    json.dump({str(k): v for k, v in res.items()}, open("../results/commitment_results.json", "w"))

    # by p2 at alpha2 = 0.3 (alignment unchanged)
    for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
        lab = [outcome(0.3, t, p) for t in grid]
        print("p2", p, "breakdown share over theta2:", round(lab.count("breakdown") / len(lab), 3))
