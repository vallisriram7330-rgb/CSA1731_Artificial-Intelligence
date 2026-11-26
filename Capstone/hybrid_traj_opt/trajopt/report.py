"""Generates REPORT.md from the measured results (all numbers come from the run)."""
import numpy as np


def write(path, prob, cfg, args, table, finals, times, best_name):
    b, bm = table["Baseline (quintic)"], table["Baseline (matched time)"]
    algs = ["PSO", "GWO", "Hybrid PSO-GWO"]
    means = {n: np.mean(finals[n]) for n in algs}
    stds = {n: np.std(finals[n]) for n in algs}
    rank = sorted(algs, key=lambda n: means[n])
    h = table["Hybrid PSO-GWO"]
    spread_pct = 100 * (means[rank[-1]] - means[rank[0]]) / means[rank[0]]
    noise = max(stds.values())

    if rank[0] == "Hybrid PSO-GWO":
        verdict = (f"The hybrid method achieved the lowest mean cost ({means['Hybrid PSO-GWO']:.4f}) over "
                   f"{args.runs} independent runs.")
    else:
        verdict = (f"The hybrid method did NOT achieve the lowest mean cost; {rank[0]} did "
                   f"({means[rank[0]]:.4f} vs {means['Hybrid PSO-GWO']:.4f} for the hybrid).")
    if spread_pct < 2 * 100 * noise / means[rank[0]]:
        sig = ("The gap between the three optimisers is of the same size as the run-to-run spread, so the "
               "ranking should be regarded as indicative, not conclusive. More runs would be needed for a "
               "statistical test.")
    else:
        sig = "The gap between optimisers is larger than the run-to-run spread."

    L = []
    A = L.append
    A("# Hybrid AI-Based Trajectory Optimization for Energy-Efficient Robotic Manipulator Control using PSO and GWO\n")
    A("*Auto-generated from the simulation run. Every number below was measured by `main.py`.*\n")
    A("## 1. Objective\nFind a joint-space trajectory that moves a 2-DOF robotic arm from a start pose to a target pose "
      "with **low energy use, low positioning error, smooth motion and short duration**, while respecting joint "
      "angle, velocity, acceleration and torque limits. Three metaheuristics are compared: PSO, GWO and a hybrid PSO-GWO.\n")
    A("## 2. Method\n"
      "**Robot.** 2-link planar arm in a vertical plane, full Lagrangian dynamics "
      f"(link lengths {prob.model.l1} m / {prob.model.l2} m). Start joints {list(cfg.q0)} rad, goal {list(cfg.qf)} rad, "
      f"target tip position ({prob.target[0]:.3f}, {prob.target[1]:.3f}) m.\n")
    A("**Trajectory parameterisation (7 decision variables).** Each joint = quintic polynomial (baseline) + 3 shape "
      "functions that vanish (with velocity and acceleration) at both ends, plus the motion duration T. "
      "The arm therefore always starts and stops at rest; the optimiser only reshapes the path between.\n")
    A("**Simulation / measurement.** Every candidate is run through a computed-torque + PID controller on a "
      "*plant that differs from the controller's model* "
      f"(payload {cfg.payload_true} kg vs {cfg.payload_model} kg assumed, joint friction), with torque saturation. "
      "Energy and final position error are measured on this simulated plant, so they are not trivially zero.\n")
    A("**Energy estimate.** E = ∫ Σᵢ [ max(τᵢ·ωᵢ, 0) + R·τᵢ² ] dt, with R = "
      f"{cfg.R_loss} (positive mechanical work + copper loss; no energy recovery). It is a model-based *estimate*, not a "
      "hardware measurement.\n")
    A(
      f"**Cost.**  J = {cfg.w[0]}·E/E_ref + {cfg.w[1]}·err/{cfg.err_ref*1000:.0f} mm + {cfg.w[2]}·jerk/jerk_ref "
      f"+ {cfg.w[3]}·T/{cfg.T_baseline} s + {cfg.penalty:.0f}·(constraint violation); E_ref and jerk_ref come from the baseline "
      "(T = 3 s quintic). The weights are a design choice and change the outcome.\n")
    A("**Algorithms** (identical budget: population %d × %d iterations, same initial population per seed, %d independent runs).\n"
      % (args.pop, args.iters, args.runs))
    A("* **PSO** – inertia 0.9→0.4, c1 = c2 = 2.\n"
      "* **GWO** – alpha/beta/delta leaders, coefficient a: 2→0.\n"
      "* **Hybrid PSO-GWO** – the three best personal bests act as GWO leaders; their guide points are averaged and replace "
      "PSO's global best: `v = w·v + c1·r1·(pbest − x) + c2·r2·(X_gwo − x)`. GWO gives wide exploration early, PSO gives "
      "momentum and memory for fine convergence.\n")
    A("## 3. Results\n")
    A("| Method | Energy [J] | vs baseline | Final error [mm] | RMS jerk [rad/s³] | Duration [s] | Cost | Cost mean ± std (runs) |")
    A("|---|---|---|---|---|---|---|---|")
    for k, r in table.items():
        A(f"| {k} | {r['energy']:.1f} | {r['energy_pct']:+.1f}% | {r['error_mm']:.2f} | {r['jerk']:.2f} | {r['T']:.2f} | "
          f"{r['cost']:.4f} | {r['cost_mean']} |")
    A("\n*The table shows the best run of each optimiser; the last column covers all runs.*\n")
    A("![Convergence](fig_convergence.png)\n![Metrics](fig_bars.png)\n![Trajectories](fig_trajectories.png)\n"
      "![Torques](fig_torques.png)\n![End-effector path](fig_workspace.png)\n![Spread](fig_boxplot.png)\n")
    A("## 4. Discussion (generated from the numbers)\n")
    o = table[best_name]
    d_time = bm["energy"] - b["energy"]     # effect of changing duration only (same quintic shape)
    d_shape = o["energy"] - bm["energy"]    # effect of reshaping the path at that duration
    word = lambda x: "increases" if x > 0 else "reduces"
    A(f"* **Energy.** The best optimiser by mean cost ({best_name}) uses {o['energy']:.1f} J versus {b['energy']:.1f} J for the "
      f"{cfg.T_baseline:.0f} s quintic baseline ({o['energy_pct']:+.1f}%). To separate causes: running the *same quintic* at the optimised "
      f"duration ({bm['T']:.2f} s) {word(d_time)} energy by {abs(d_time):.1f} J (to {bm['energy']:.1f} J), and the optimised path *shape* then "
      f"{word(d_shape)} it by a further {abs(d_shape):.1f} J ({100*d_shape/bm['energy']:+.1f}% relative to the matched-duration baseline).")
    A(f"* **Accuracy.** Final error {o['error_mm']:.2f} mm (baseline {b['error_mm']:.2f} mm, "
      f"matched-time baseline {bm['error_mm']:.2f} mm).")
    sm = "lower (smoother)" if o["jerk"] < b["jerk"] else "higher (less smooth)"
    A(f"* **Smoothness.** RMS jerk is {o['jerk']:.2f} vs {b['jerk']:.2f} rad/s³ for the baseline ({sm}); the optimised duration is "
      f"{o['T']:.2f} s vs {b['T']:.2f} s. Smoothness, energy, accuracy and time are traded off through the cost weights, so a different weighting "
      "would give a different compromise.")
    A(f"* **Constraints.** All reported solutions have constraint violation = "
      f"{max(r['violation'] for r in table.values()):.3f} (0 means every limit satisfied).")
    A(f"* **Algorithm ranking (mean cost, lower is better).** " +
      " < ".join(f"{n} ({means[n]:.4f} ± {stds[n]:.4f})" for n in rank) + ". " + verdict + " " + sig)
    A(f"* **Computation time per optimisation run:** " + ", ".join(f"{n} {times[n]:.1f} s" for n in algs) + ".\n")
    A("## 5. Limitations\n"
      "* Simulation only; a 2-DOF planar arm; the energy model is simplified and not validated on hardware.\n"
      "* Results depend on the cost weights, the controller gains and the plant mismatch assumed.\n"
      "* A single start/goal pair was tested; other motions or more DOFs may rank the algorithms differently.\n"
      "* Hybrid design is one of many possible PSO-GWO combinations.\n")
    A("## 6. How to reproduce\n```\npip install -r requirements.txt\npython main.py            # full experiment (about 8-15 min on one CPU core)\npython main.py --quick    # smoke test\n```\n")
    open(path, "w", encoding="utf-8").write("\n".join(L))
