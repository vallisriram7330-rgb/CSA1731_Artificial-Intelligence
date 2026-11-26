"""2-link planar manipulator (vertical plane) with full rigid-body dynamics.

All functions are vectorised: q, qd, qdd, tau may have any leading batch shape and a
last axis of size 2.
"""
import numpy as np

GRAV = 9.81


class Arm2R:
    def __init__(self, m1=3.0, m2=2.0, l1=0.5, l2=0.4, payload=0.0, viscous=(0.0, 0.0)):
        self.l1, self.l2 = l1, l2
        lc1, lc2 = l1 / 2.0, l2 / 2.0
        I1, I2 = m1 * l1 ** 2 / 12.0, m2 * l2 ** 2 / 12.0
        # fold a point payload at the tip into link 2
        M2 = m2 + payload
        lc2n = (m2 * lc2 + payload * l2) / M2
        I2n = I2 + m2 * (lc2n - lc2) ** 2 + payload * (l2 - lc2n) ** 2
        self.a1 = I1 + I2n + m1 * lc1 ** 2 + M2 * (l1 ** 2 + lc2n ** 2)
        self.a2 = M2 * l1 * lc2n
        self.a3 = I2n + M2 * lc2n ** 2
        self.g1c = (m1 * lc1 + M2 * l1) * GRAV
        self.g2c = M2 * lc2n * GRAV
        self.fv = np.asarray(viscous, dtype=float)

    # ---------------- kinematics ----------------
    def fk(self, q):
        q = np.asarray(q)
        x = self.l1 * np.cos(q[..., 0]) + self.l2 * np.cos(q[..., 0] + q[..., 1])
        y = self.l1 * np.sin(q[..., 0]) + self.l2 * np.sin(q[..., 0] + q[..., 1])
        return np.stack([x, y], axis=-1)

    def joint_positions(self, q):
        """Return (elbow, tip) Cartesian points for a single configuration."""
        e = np.array([self.l1 * np.cos(q[0]), self.l1 * np.sin(q[0])])
        t = self.fk(q)
        return e, t

    # ---------------- dynamics ----------------
    def bias(self, q, qd):
        s2, c12 = np.sin(q[..., 1]), np.cos(q[..., 0] + q[..., 1])
        b1 = (-self.a2 * s2 * (2 * qd[..., 0] * qd[..., 1] + qd[..., 1] ** 2)
              + self.g1c * np.cos(q[..., 0]) + self.g2c * c12)
        b2 = self.a2 * s2 * qd[..., 0] ** 2 + self.g2c * c12
        return np.stack([b1, b2], axis=-1) + self.fv * qd

    def inverse_dynamics(self, q, qd, qdd):
        c2 = np.cos(q[..., 1])
        m11 = self.a1 + 2 * self.a2 * c2
        m12 = self.a3 + self.a2 * c2
        t1 = m11 * qdd[..., 0] + m12 * qdd[..., 1]
        t2 = m12 * qdd[..., 0] + self.a3 * qdd[..., 1]
        return np.stack([t1, t2], axis=-1) + self.bias(q, qd)

    def forward_accel(self, q, qd, tau):
        c2 = np.cos(q[..., 1])
        m11 = self.a1 + 2 * self.a2 * c2
        m12 = self.a3 + self.a2 * c2
        m22 = self.a3
        r = tau - self.bias(q, qd)
        det = m11 * m22 - m12 ** 2
        a1 = (m22 * r[..., 0] - m12 * r[..., 1]) / det
        a2 = (-m12 * r[..., 0] + m11 * r[..., 1]) / det
        return np.stack([a1, a2], axis=-1)
