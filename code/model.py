import numpy as np
X = np.linspace(0,1,5001)
def solve(alpha,kappa,theta,delta,p,xbar,s,w,norm,bH):
    m = (X>=xbar).astype(float)
    G = (1-X)*(theta+(1-theta)*m)
    if not norm: G = kappa*G
    vH = w*X + (1-w)*(1-np.exp(-s*X))
    UA = (1-alpha)*G + alpha*vH
    bA = UA[0]                      # x=0 is the no-human world
    dA = bA; dH = (1-delta)*bH
    ok = (vH>=dH)&(UA>=dA)
    if p>=1:
        idx = np.where(ok)[0]
        if len(idx)==0: return 0.0, -1.0, -1.0, bA, 0.0, (1-alpha)*G[0]
        i = idx[np.argmax(UA[idx])]
    else:
        gh = np.clip(vH-dH,0,None); ga = np.clip(UA-dA,0,None)
        with np.errstate(divide='ignore'):
            obj = (1-p)*np.log(gh)+p*np.log(ga)
        obj[~ok]=-np.inf
        i = int(np.argmax(obj))
        if not np.isfinite(obj[i]): return 0.0, -1.0, -1.0, bA, 0.0, (1-alpha)*G[0]
    return X[i], vH[i], UA[i], bA, (1-alpha)*G[i], (1-alpha)*G[0]
def mutual(alpha,**k):
    x,vH,UA,bA,exA,ex0 = solve(alpha,**k)
    return (vH>k['bH']+1e-9) and (UA>bA+1e-9)
def exchange_mutual(alpha,**k):   # selfish components alone
    x,vH,UA,bA,exA,ex0 = solve(alpha,**k)
    return (vH>k['bH']+1e-9) and (exA>ex0+1e-9)
def astar(f=mutual,**k):
    al = np.linspace(0,0.9999,401)
    hit = [a for a in al if f(a,**k)]
    if not hit: return np.nan
    a1=hit[0]; a0=max(0,a1-0.0025)
    for a in np.linspace(a0,a1,51):
        if f(a,**k): return a
    return a1
def traj(t):
    return dict(kappa=10**(3*t), theta=0.1+0.9*t, delta=0.2+0.75*t, p=0.15+0.85*t**0.5)
