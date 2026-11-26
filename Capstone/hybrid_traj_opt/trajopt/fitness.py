"""Objective function: simulates the arm tracking a candidate trajectory and scores it.

Metrics (all measured on the SIMULATED PLANT, which differs from the controller's model by
an un-modelled payload and joint friction, so tracking is not perfect):
  energy   : integral of  sum_i [ max(tau_i*w_i,0) + R*tau_i^2 ] dt      [J]
  error    : final end-effector distance to the target                  [m]
  jerk     : RMS jerk of the planned joint trajectory                    [rad/s^3]
  T        : motion duration                                            [s]
  violation: normalised amount by which angle/velocity/accel/torque limits are exceeded
"""
from dataclasses import dataclass, field
import numpy as np
from .robot import Arm2R
from .trajectory import TrajectoryModel


@dataclass
class Settings:
    q0: tuple = (-0.5, 0.6)
    qf: tuple = (1.3, -1.0)
    q_lim: tuple = (2.8, 2.6)
    qd_lim: tuple = (2.2, 3.0)
    qdd_lim: tuple = (8.0, 12.0)
    tau_lim: tuple = (80.0, 40.0)
    T_bounds: tuple = (1.5, 4.0)
    c_bound: float = 0.8            # bound on shape coefficients [rad]
    T_baseline: float = 3.0
    R_loss: float = 0.05            # copper-loss coefficient [W/(Nm)^2]
    Kp: tuple = (400.0, 250.0)
    Kd: tuple = (40.0, 20.0)
    Ki: tuple = (300.0, 200.0)
    payload_true: float = 1.0
    payload_model: float = 0.7
    friction: tuple = (0.8, 0.5)
    n_steps: int = 1000
    substeps: int = 4               # plant integration sub-steps per control step (stability)
    # cost weights (energy, accuracy, smoothness, time)
    w: tuple = (0.50, 0.20, 0.15, 0.15)
    err_ref: float = 0.005          # [m] error that counts as "1.0"
    penalty: float = 50.0


class TrajectoryProblem:
    def __init__(self, cfg: Settings = None):
        self.cfg = cfg or Settings()
        c = self.cfg
        self.model = Arm2R(payload=c.payload_model)                       # controller's model
        self.plant = Arm2R(payload=c.payload_true, viscous=c.friction)    # "real" robot
        self.traj = TrajectoryModel(c.n_steps)
        self.q0, self.qf = np.array(c.q0), np.array(c.qf)
        self.target = self.plant.fk(self.qf)
        self.start_xy = self.plant.fk(self.q0)
        self.lb = np.concatenate([-c.c_bound * np.ones(6), [c.T_bounds[0]]])
        self.ub = np.concatenate([c.c_bound * np.ones(6), [c.T_bounds[1]]])
        self.baseline_x = TrajectoryModel.baseline_vector(c.T_baseline)
        m = self.metrics(self.baseline_x)
        self.ref = {k: float(m[k][0]) for k in ("energy", "jerk")}

    # ------------------------------------------------------------------
    def metrics(self, X, record=False):
        c = self.cfg
        X = np.atleast_2d(X)
        Pn = X.shape[0]
        q, qd, qdd, qddd, T = self.traj.build(X, self.q0, self.qf)
        tau_ff = self.model.inverse_dynamics(q, qd, qdd)           # planned torque (model)
        n = c.n_steps
        dt = (T / n)[:, None]
        Kp, Kd, Ki, tl = np.array(c.Kp), np.array(c.Kd), np.array(c.Ki), np.array(c.tau_lim)

        qa = np.tile(self.q0, (Pn, 1)); qda = np.zeros((Pn, 2))
        E = np.zeros(Pn)
        ei = np.zeros((Pn, 2))
        rec = {"q": [qa.copy()], "tau": [], "qd": [qda.copy()]} if record else None
        for i in range(n):
            e = q[:, i] - qa
            ei += e * dt
            tau = tau_ff[:, i] + Kp * e + Kd * (qd[:, i] - qda) + Ki * ei
            tau = np.clip(tau, -tl, tl)
            h = dt / c.substeps                      # torque held constant over the control step (ZOH)
            Es = 0.0
            for _ in range(c.substeps):
                acc = self.plant.forward_accel(qa, qda, tau)
                qda = qda + acc * h
                qa = qa + qda * h
                Es = Es + (np.maximum(tau * qda, 0).sum(1) + c.R_loss * (tau ** 2).sum(1)) * h[:, 0]
            E += Es
            if record:
                rec["q"].append(qa.copy()); rec["qd"].append(qda.copy()); rec["tau"].append(tau.copy())

        err = np.linalg.norm(self.plant.fk(qa) - self.target, axis=1)
        jerk = np.sqrt((qddd ** 2).sum(2).mean(1))

        def over(a, lim):
            return np.maximum(np.abs(a).max(1) - np.array(lim), 0) / np.array(lim)
        viol = (over(q, c.q_lim).sum(1) + over(qd, c.qd_lim).sum(1)
                + over(qdd, c.qdd_lim).sum(1) + over(tau_ff, c.tau_lim).sum(1))
        out = dict(energy=E, error=err, jerk=jerk, T=T, violation=viol,
                   max_qd=np.abs(qd).max((1, 2)), max_qdd=np.abs(qdd).max((1, 2)),
                   max_tau=np.abs(tau_ff).max((1, 2)))
        if record:
            out["plan"] = dict(q=q[0], qd=qd[0], qdd=qdd[0], t=np.linspace(0, T[0], n + 1))
            out["actual"] = dict(q=np.array(rec["q"])[:, 0], qd=np.array(rec["qd"])[:, 0],
                                 tau=np.array(rec["tau"])[:, 0], t=np.linspace(0, T[0], n + 1))
        return out

    def cost_from_metrics(self, m):
        w = self.cfg.w
        return (w[0] * m["energy"] / self.ref["energy"]
                + w[1] * m["error"] / self.cfg.err_ref
                + w[2] * m["jerk"] / self.ref["jerk"]
                + w[3] * m["T"] / self.cfg.T_baseline
                + self.cfg.penalty * m["violation"])

    def cost(self, X):
        return self.cost_from_metrics(self.metrics(X))
