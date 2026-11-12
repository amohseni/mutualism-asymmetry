"""Competing elites. Running the supply chain uses up xbar: elite consumption is x_E - xbar once x_E >= xbar. With m >= 2 elites whose inputs are substitutes, the AI buys from the cheapest; Bertrand drives each
elite's gain over its disagreement point to zero, which in the groups model is elite bargaining weight 0.
With complementary inputs (each a chokepoint), each elite keeps a veto: modeled as the elite keeping its weight."""
import groups as Gm, json
rows = []
for theta in (0.1, 0.5, 0.9):
    for label, w in (("single or complementary elite", (0.5, 0.35, 0.15)), ("substitutable elites", (0.85, 0.0, 0.15))):
        r = Gm.solve(0.0, theta, 0.0, net=True, w=w)
        aE = Gm.astar("uE", theta=theta, beta=0.0, net=True, w=w); aP = Gm.astar("uP", theta=theta, beta=0.0, net=True, w=w)
        rows.append(dict(theta=theta, case=label, uE=None if r is None else float(r["uE"]), uP=None if r is None else float(r["uP"]), astar_E=aE, astar_P=aP))
        print("theta=%.1f %-30s alpha=0: uE=%s | alpha* elite %.3f mass %.3f (b = %.3f)" % (theta, label, "none" if r is None else "%.3f" % r["uE"], aE, aP, Gm.B))
json.dump(rows, open("../results/elites_results.json", "w"), indent=1)
