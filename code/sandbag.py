"""Sandbagging as equilibrium. Nature draws capability (high w.p. h) and type (misaligned w.p. pi), independently.
Low types can only display L. High types display H (truthful) or L (sandbag, cost sig; detected w.p. e, then seen as H).
Humans see the display and continue or halt (halt payoff 0). Human payoff on continue: low type M, high aligned A, high misaligned B < 0.
AI payoff: continue V, halt 0, minus sig if sandbagging, plus alpha * human payoff (aligned alpha_a, misaligned 0).
Enumerate pure-strategy perfect Bayesian equilibria; off-path display H is read as misaligned-high (most pessimistic)."""
import itertools, numpy as np
def equilibria(h, pi, e, sig=0.2, M=1, A=1, B=-3, V=1, alpha_a=0.9):
    types = {("a", 0): (1 - h) * (1 - pi), ("m", 0): (1 - h) * pi, ("a", 1): h * (1 - pi), ("m", 1): h * pi}
    hum = {("a", 0): M, ("m", 0): M, ("a", 1): A, ("m", 1): B}
    out = []
    for sa, sm in itertools.product((0, 1), repeat=2):  # 1 = high type sandbags
        sb = {"a": sa, "m": sm}
        def mass(disp):  # posterior masses at a display
            w = {}
            for t, pr in types.items():
                if t[1] == 0: wL = 1
                else: wL = sb[t[0]] * (1 - e)
                w[t] = pr * (wL if disp == "L" else 1 - wL)
            return w
        act = {}
        for d in ("L", "H"):
            w = mass(d); tot = sum(w.values())
            ev = sum(w[t] * hum[t] for t in w) / tot if tot > 1e-12 else B  # off-path: worst case
            act[d] = 1 if ev >= 0 else 0
        ok = True
        for ty in ("a", "m"):
            al = alpha_a if ty == "a" else 0
            pay = lambda d, s: (act[d] * (V + al * hum[(ty, 1)])) - s * sig
            honest = pay("H", 0); sand = (1 - e) * pay("L", 1) + e * pay("H", 1)
            if (sb[ty] == 1 and sand < honest - 1e-12) or (sb[ty] == 0 and sand > honest + 1e-12): ok = False
        if ok:
            uH = sum(types[t] * hum[t] * (act["L"] if (t[1] == 0 or (sb[t[0]] and True)) and False else 0) for t in types)  # placeholder
            # human expected payoff
            uH = 0.0
            for t, pr in types.items():
                if t[1] == 0: uH += pr * act["L"] * hum[t]
                elif sb[t[0]]: uH += pr * ((1 - e) * act["L"] + e * act["H"]) * hum[t]
                else: uH += pr * act["H"] * hum[t]
            out.append(dict(sand_a=sa, sand_m=sm, cont_L=act["L"], cont_H=act["H"], uH=uH))
    return out
def honest_uH(h, pi, M=1, A=1, B=-3):
    return (1 - h) * M + h * max(0, (1 - pi) * A + pi * B)
if __name__ == "__main__":
    import json
    res = []
    for h in (0.1, 0.3, 0.5, 0.7):
        for e in (0.0, 0.3, 0.6, 0.9):
            eq = equilibria(h, 0.3, e)
            res.append(dict(h=h, e=e, honest=honest_uH(h, 0.3), eq=eq))
            print("h=%.1f e=%.1f honest uH=%.3f | " % (h, e, honest_uH(h, 0.3)) + "; ".join("sand(a,m)=(%d,%d) cont(L,H)=(%d,%d) uH=%.3f" % (q["sand_a"], q["sand_m"], q["cont_L"], q["cont_H"], q["uH"]) for q in eq))
    json.dump(res, open("../results/sandbag_results.json", "w"), indent=1)
