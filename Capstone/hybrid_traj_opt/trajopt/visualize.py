"""All plots and the robot-arm animation."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

COL = {"Baseline (quintic)": "#6b7280", "Baseline (matched time)": "#9ca3af",
       "PSO": "#2563eb", "GWO": "#16a34a", "Hybrid PSO-GWO": "#dc2626"}


def convergence(hists, path):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for name, H in hists.items():
        H = np.array(H); m, s = H.mean(0), H.std(0)
        ax.plot(m, label=name, color=COL[name], lw=2)
        ax.fill_between(range(len(m)), m - s, m + s, color=COL[name], alpha=0.15)
    ax.set_xlabel("Iteration"); ax.set_ylabel("Best cost (lower is better)")
    ax.set_title("Optimisation progress (mean ± std over runs)")
    ax.grid(alpha=.3); ax.legend(); fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def trajectories(base, opt, opt_name, path):
    fig, axs = plt.subplots(3, 2, figsize=(10, 8), sharex=False)
    for j in range(2):
        for r, (key, lab) in enumerate([("q", "Angle [rad]"), ("qd", "Velocity [rad/s]"),
                                        ("qdd", "Accel. [rad/s²]")]):
            ax = axs[r, j]
            ax.plot(base["plan"]["t"], base["plan"][key][:, j], color=COL["Baseline (quintic)"], lw=2, label="Baseline")
            ax.plot(opt["plan"]["t"], opt["plan"][key][:, j], color=COL[opt_name], lw=2, label=opt_name)
            ax.set_ylabel(lab); ax.grid(alpha=.3)
            if r == 0: ax.set_title(f"Joint {j+1}")
            if r == 2: ax.set_xlabel("Time [s]")
    axs[0, 0].legend(); fig.suptitle("Planned joint trajectories: baseline vs optimised"); fig.tight_layout()
    fig.savefig(path, dpi=150); plt.close(fig)


def torques(base, opt, opt_name, path):
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    for j in range(2):
        axs[j].plot(base["actual"]["t"][1:], base["actual"]["tau"][:, j], color=COL["Baseline (quintic)"], lw=2, label="Baseline")
        axs[j].plot(opt["actual"]["t"][1:], opt["actual"]["tau"][:, j], color=COL[opt_name], lw=2, label=opt_name)
        axs[j].set_title(f"Joint {j+1} motor torque"); axs[j].set_xlabel("Time [s]")
        axs[j].set_ylabel("Torque [Nm]"); axs[j].grid(alpha=.3)
    axs[0].legend(); fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def bars(table, path):
    names = list(table)
    items = [("energy", "Energy [J]"), ("error_mm", "Final error [mm]"),
             ("jerk", "RMS jerk [rad/s³]"), ("T", "Duration [s]")]
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.8))
    for ax, (k, lab) in zip(axs, items):
        vals = [table[n][k] for n in names]
        ax.bar(range(len(names)), vals, color=[COL[n] for n in names])
        ax.set_xticks(range(len(names))); ax.set_xticklabels([n.replace(" ", "\n", 1) for n in names], fontsize=7)
        ax.set_title(lab); ax.grid(axis="y", alpha=.3)
        for i, v in enumerate(vals): ax.text(i, v, f"{v:.2f}", ha="center", va="bottom", fontsize=7)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def boxplot(final_costs, path):
    fig, ax = plt.subplots(figsize=(6, 4))
    names = list(final_costs)
    bp = ax.boxplot([final_costs[n] for n in names], labels=names, patch_artist=True)
    for patch, n in zip(bp["boxes"], names): patch.set_facecolor(COL[n]); patch.set_alpha(.6)
    ax.set_ylabel("Final best cost"); ax.set_title("Result spread over independent runs"); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def workspace(problem, rec_base, rec_opt, opt_name, path):
    arm = problem.plant
    fig, ax = plt.subplots(figsize=(5.2, 5))
    for rec, name, ls in [(rec_base, "Baseline (quintic)", "--"), (rec_opt, opt_name, "-")]:
        xy = arm.fk(rec["actual"]["q"]); ax.plot(xy[:, 0], xy[:, 1], ls, color=COL[name], lw=2, label=f"{name} tip path")
    for q, a in [(problem.q0, .35), (problem.qf, .9)]:
        e, t = arm.joint_positions(q); ax.plot([0, e[0], t[0]], [0, e[1], t[1]], "o-", color="k", alpha=a, lw=3)
    ax.plot(*problem.target, "r*", ms=14, label="Target")
    ax.set_aspect("equal"); ax.grid(alpha=.3); ax.legend(fontsize=7); ax.set_title("End-effector path (start/goal poses shown)")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def animate(problem, rec_base, rec_opt, opt_name, path, frames=60):
    arm = problem.plant
    fig, axs = plt.subplots(1, 2, figsize=(9, 4.4))
    sets = [(rec_base, "Baseline (quintic)"), (rec_opt, opt_name)]
    lines, trails, txts = [], [], []
    for ax, (rec, name) in zip(axs, sets):
        ax.set_xlim(-0.2, 1.0); ax.set_ylim(-0.4, 0.9); ax.set_aspect("equal"); ax.grid(alpha=.3)
        ax.plot(*problem.target, "r*", ms=12)
        ln, = ax.plot([], [], "o-", color=COL[name], lw=4, ms=7)
        tr, = ax.plot([], [], color=COL[name], lw=1, alpha=.6)
        tx = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=8, va="top")
        ax.set_title(f"{name}  (T={rec['actual']['t'][-1]:.2f}s)", fontsize=9)
        lines.append(ln); trails.append(tr); txts.append(tx)
    tips = [arm.fk(r["actual"]["q"]) for r, _ in sets]

    Tmax = max(r["actual"]["t"][-1] for r, _ in sets)

    def draw(f):
        clock = f / (frames - 1) * Tmax          # real-time clock: the faster motion finishes first
        for k, (rec, _) in enumerate(sets):
            tt = rec["actual"]["t"]
            i = min(int(np.searchsorted(tt, clock)), len(tt) - 1)
            q = rec["actual"]["q"][i]; e, t = arm.joint_positions(q)
            lines[k].set_data([0, e[0], t[0]], [0, e[1], t[1]])
            trails[k].set_data(tips[k][:i + 1, 0], tips[k][:i + 1, 1])
            txts[k].set_text(f"t = {min(clock, tt[-1]):.2f}s")
        return lines + trails + txts
    anim = FuncAnimation(fig, draw, frames=frames, interval=60, blit=False)
    anim.save(path, writer=PillowWriter(fps=15)); plt.close(fig)
