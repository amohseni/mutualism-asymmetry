"""Is the set of alpha giving mutualism an upper interval [alpha*, 1)? Needed for bisection."""
import numpy as np
from scipy.stats import qmc
from sweep import back, mutual, PARAMS
U = qmc.Sobol(d=len(PARAMS), scramble=True, seed=7).random(512)
al = np.linspace(0, 0.9999, 201); bad = 0
for norm in (False, True):
    for u in U:
        k = back(u); k["norm"] = norm
        f = np.array([mutual(a, **k) for a in al])
        if f.any():
            first = np.argmax(f)
            if not f[first:].all(): bad += 1
print("non-monotone points:", bad, "of", 2 * len(U))
