"""PSO, GWO and the hybrid PSO-GWO (HPSOGWO) optimisers.

All take a *batched* objective  f(X[P,D]) -> cost[P]  and share the same budget
(population x iterations) and the same initial population when given the same seed.
"""
import numpy as np


def _init(lb, ub, pop, rng):
    return lb + rng.random((pop, lb.size)) * (ub - lb)


def _result(gx, gf, hist):
    return dict(best_x=gx.copy(), best_f=float(gf), history=np.array(hist))


def pso(f, lb, ub, pop=30, iters=60, seed=0, w_max=0.9, w_min=0.4, c1=2.0, c2=2.0):
    rng = np.random.default_rng(seed)
    x = _init(lb, ub, pop, rng); vmax = 0.5 * (ub - lb)
    v = np.zeros_like(x)
    fx = f(x)
    pb, pbf = x.copy(), fx.copy()
    g = pbf.argmin(); gx, gf = pb[g].copy(), pbf[g]
    hist = [gf]
    for t in range(iters):
        w = w_max - (w_max - w_min) * t / iters
        r1, r2 = rng.random(x.shape), rng.random(x.shape)
        v = np.clip(w * v + c1 * r1 * (pb - x) + c2 * r2 * (gx - x), -vmax, vmax)
        x = np.clip(x + v, lb, ub)
        fx = f(x)
        imp = fx < pbf
        pb[imp], pbf[imp] = x[imp], fx[imp]
        g = pbf.argmin()
        if pbf[g] < gf:
            gx, gf = pb[g].copy(), pbf[g]
        hist.append(gf)
    return _result(gx, gf, hist)


def _leaders_move(x, fx, a, rng):
    """GWO step: candidate positions X1,X2,X3 guided by alpha, beta, delta."""
    order = np.argsort(fx)[:3]
    cands = []
    for k in order:
        leader = x[k]
        A = 2 * a * rng.random(x.shape) - a
        C = 2 * rng.random(x.shape)
        cands.append(leader - A * np.abs(C * leader - x))
    return cands


def gwo(f, lb, ub, pop=30, iters=60, seed=0):
    rng = np.random.default_rng(seed)
    x = _init(lb, ub, pop, rng)
    fx = f(x)
    g = fx.argmin(); gx, gf = x[g].copy(), fx[g]
    hist = [gf]
    for t in range(iters):
        a = 2.0 * (1 - t / iters)
        X1, X2, X3 = _leaders_move(x, fx, a, rng)
        x = np.clip((X1 + X2 + X3) / 3.0, lb, ub)
        fx = f(x)
        g = fx.argmin()
        if fx[g] < gf:
            gx, gf = x[g].copy(), fx[g]
        hist.append(gf)
    return _result(gx, gf, hist)


def hybrid_pso_gwo(f, lb, ub, pop=30, iters=60, seed=0, w_max=0.9, w_min=0.4, c1=1.5, c2=1.5):
    """Hybrid PSO-GWO.

    * GWO part  : the three best personal-best positions act as alpha, beta, delta wolves.
                  They generate three guide points X1, X2, X3 (shrinking coefficient a: 2 -> 0)
                  whose mean  X_gwo = (X1+X2+X3)/3  replaces PSO's single global best.
    * PSO part  : every particle keeps inertia (w: 0.9 -> 0.4) and its own personal best.

        v <- w*v + c1*r1*(pbest - x) + c2*r2*(X_gwo - x),      x <- x + v

    Result: wolf-style exploration early (many leaders, large random steps), particle-style
    memory/momentum for fine convergence late.
    """
    rng = np.random.default_rng(seed)
    x = _init(lb, ub, pop, rng); vmax = 0.5 * (ub - lb)
    v = np.zeros_like(x)
    fx = f(x)
    pb, pbf = x.copy(), fx.copy()
    g = pbf.argmin(); gx, gf = pb[g].copy(), pbf[g]
    hist = [gf]
    for t in range(iters):
        a = 2.0 * (1 - t / iters)
        w = w_max - (w_max - w_min) * t / iters
        order = np.argsort(pbf)[:3]
        guides = []
        for k in order:
            A = 2 * a * rng.random(x.shape) - a
            C = 2 * rng.random(x.shape)
            guides.append(pb[k] - A * np.abs(C * pb[k] - x))
        x_gwo = sum(guides) / 3.0
        v = np.clip(w * v + c1 * rng.random(x.shape) * (pb - x)
                    + c2 * rng.random(x.shape) * (x_gwo - x), -vmax, vmax)
        x = np.clip(x + v, lb, ub)
        fx = f(x)
        imp = fx < pbf
        pb[imp], pbf[imp] = x[imp], fx[imp]
        g = pbf.argmin()
        if pbf[g] < gf:
            gx, gf = pb[g].copy(), pbf[g]
        hist.append(gf)
    return _result(gx, gf, hist)


ALGORITHMS = {"PSO": pso, "GWO": gwo, "Hybrid PSO-GWO": hybrid_pso_gwo}
