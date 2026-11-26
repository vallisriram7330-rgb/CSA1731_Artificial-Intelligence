"""Trajectory parameterisation.

Each joint follows   q(s) = q0 + (qf-q0)*Quintic(s) + sum_k c_k * B_k(s),   s = t/T in [0,1]

* Quintic(s) = 10 s^3 - 15 s^4 + 6 s^5  (classic smooth point-to-point profile = BASELINE)
* B_k(s) = 64 s^3 (1-s)^3 (2s-1)^k      (k = 0,1,2) are shape functions whose value, velocity
  and acceleration vanish at both ends, so the arm always starts/stops at rest at the
  right place, while the optimiser reshapes the path in between.

Decision vector per candidate:  [c_(j1,k0..2), c_(j2,k0..2), T]   (7 variables)
"""
import numpy as np
from numpy.polynomial import Polynomial as P

N_BASIS = 3


def _basis_polys():
    quintic = P([0, 0, 0, 10, -15, 6])
    base = 64 * P([0, 0, 0, 1]) * P([1, -1]) ** 3
    shapes = [base * P([-1, 2]) ** k for k in range(N_BASIS)]
    return quintic, shapes


class TrajectoryModel:
    def __init__(self, n_steps=400):
        self.n = n_steps
        s = np.linspace(0.0, 1.0, n_steps + 1)
        quintic, shapes = _basis_polys()
        self.Q = np.stack([quintic.deriv(m)(s) if m else quintic(s) for m in range(4)])       # (4, n+1)
        self.B = np.stack([[sh.deriv(m)(s) if m else sh(s) for sh in shapes] for m in range(4)])  # (4,K,n+1)
        self.n_var = 2 * N_BASIS + 1

    def build(self, X, q0, qf):
        """X: (P, 7).  Returns q, qd, qdd, qddd of shape (P, n+1, 2) and T of shape (P,)."""
        X = np.atleast_2d(X)
        C = X[:, :2 * N_BASIS].reshape(-1, 2, N_BASIS)
        T = X[:, -1]
        dq = (np.asarray(qf) - np.asarray(q0))
        out = []
        for m in range(4):
            val = dq[None, None, :] * self.Q[m][None, :, None] + np.einsum('pjk,kn->pnj', C, self.B[m])
            if m == 0:
                val = val + np.asarray(q0)[None, None, :]
            val = val / (T[:, None, None] ** m)
            out.append(val)
        return (*out, T)

    @staticmethod
    def baseline_vector(T):
        return np.concatenate([np.zeros(2 * N_BASIS), [T]])
