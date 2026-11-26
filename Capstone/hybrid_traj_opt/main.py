"""Run the complete experiment:  python main.py [--runs 10] [--pop 30] [--iters 60] [--seed 0] [--quick]

Outputs everything into ./results :
  comparison_table.csv, summary.json, fig_*.png, arm_animation.gif, dashboard.html, REPORT.md
"""
import argparse, json, os, time
from dataclasses import asdict
import numpy as np

from trajopt.fitness import TrajectoryProblem, Settings
from trajopt.optimizers import ALGORITHMS
from trajopt import visualize as V
from trajopt import dashboard, report


def row(problem, X, label_cost=None):
    m = problem.metrics(X)
    return dict(energy=float(m["energy"][0]), error_mm=float(m["error"][0] * 1000),
                jerk=float(m["jerk"][0]), T=float(m["T"][0]), violation=float(m["violation"][0]),
                max_qd=float(m["max_qd"][0]), max_qdd=float(m["max_qdd"][0]), max_tau=float(m["max_tau"][0]),
                cost=float(problem.cost(X)[0]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--pop", type=int, default=30)
    ap.add_argument("--iters", type=int, default=60)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--quick", action="store_true", help="3 runs, 25 iterations (smoke test)")
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    if a.quick: a.runs, a.iters = 3, 25
    os.makedirs(a.out, exist_ok=True)

    cfg = Settings(); prob = TrajectoryProblem(cfg)
    print(f"Target (x,y) = {prob.target.round(3)} m | runs={a.runs} pop={a.pop} iters={a.iters}")

    # ---- baselines --------------------------------------------------------------------
    table, records, hists, finals, xs, cost_stats, times = {}, {}, {}, {}, {}, {}, {}
    table["Baseline (quintic)"] = row(prob, prob.baseline_x)
    xs["Baseline (quintic)"] = prob.baseline_x

    # ---- optimisers ---------------------------------------------------------------------
    for name, fn in ALGORITHMS.items():
        res, t0 = [], time.time()
        for r in range(a.runs):
            res.append(fn(prob.cost, prob.lb, prob.ub, pop=a.pop, iters=a.iters, seed=a.seed + r))
        times[name] = (time.time() - t0) / a.runs
        best = min(res, key=lambda d: d["best_f"])
        hists[name] = [d["history"] for d in res]
        finals[name] = [d["best_f"] for d in res]
        xs[name] = best["best_x"]
        table[name] = row(prob, best["best_x"])
        print(f"{name:16s} best={best['best_f']:.4f} mean={np.mean(finals[name]):.4f}±{np.std(finals[name]):.4f} "
              f"({times[name]:.1f}s/run)")

    # matched-duration baseline (same T as the Hybrid solution) -> separates 'slower/faster' from 'better shape'
    xm = prob.baseline_x.copy(); xm[-1] = xs["Hybrid PSO-GWO"][-1]
    table["Baseline (matched time)"] = row(prob, xm); xs["Baseline (matched time)"] = xm
    order = ["Baseline (quintic)", "Baseline (matched time)", "PSO", "GWO", "Hybrid PSO-GWO"]
    table = {k: table[k] for k in order}
    e0 = table["Baseline (quintic)"]["energy"]
    for k, r in table.items():
        r["energy_pct"] = 100 * (r["energy"] - e0) / e0
        r["cost_mean"] = (f"{np.mean(finals[k]):.4f}±{np.std(finals[k]):.4f}" if k in finals else "-")
        r["opt_time"] = f"{times[k]:.1f}" if k in times else "-"

    # ---- statistics across runs (final metrics of EVERY run, not just the best) ---------
    best_name = min(ALGORITHMS, key=lambda n: np.mean(finals[n]))   # robust: mean over runs, not one lucky run

    # ---- records for plots ----------------------------------------------------------------
    rec_b = prob.metrics(prob.baseline_x, record=True)
    rec_o = prob.metrics(xs[best_name], record=True)
    rec_o = {**rec_o}
    p = lambda f: os.path.join(a.out, f)
    V.convergence(hists, p("fig_convergence.png"))
    V.trajectories(rec_b, rec_o, best_name, p("fig_trajectories.png"))
    V.torques(rec_b, rec_o, best_name, p("fig_torques.png"))
    V.bars(table, p("fig_bars.png"))
    V.boxplot(finals, p("fig_boxplot.png"))
    V.workspace(prob, rec_b, rec_o, best_name, p("fig_workspace.png"))
    V.animate(prob, rec_b, rec_o, best_name, p("arm_animation.gif"))

    # ---- tables ---------------------------------------------------------------------------
    import csv
    with open(p("comparison_table.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["method", "energy_J", "energy_change_pct", "final_error_mm", "rms_jerk", "duration_s",
                    "total_cost", "cost_mean_std_over_runs", "optimisation_time_s_per_run",
                    "max_vel", "max_acc", "max_planned_torque", "constraint_violation"])
        for k, r in table.items():
            w.writerow([k, f"{r['energy']:.2f}", f"{r['energy_pct']:.2f}", f"{r['error_mm']:.3f}", f"{r['jerk']:.3f}",
                        f"{r['T']:.3f}", f"{r['cost']:.4f}", r["cost_mean"], r["opt_time"],
                        f"{r['max_qd']:.3f}", f"{r['max_qdd']:.3f}", f"{r['max_tau']:.2f}", f"{r['violation']:.4f}"])
    summary = dict(settings=asdict(cfg), args=vars(a), table=table,
                   final_costs={k: list(map(float, v)) for k, v in finals.items()},
                   best_vectors={k: list(map(float, v)) for k, v in xs.items()}, best_algorithm=best_name)
    with open(p("summary.json"), "w") as f: json.dump(summary, f, indent=2)

    b = table["Baseline (quintic)"]; o = table[best_name]
    kpis = [("Best method", best_name), ("Energy change", f"{o['energy_pct']:+.1f}%"),
            ("Final error", f"{o['error_mm']:.2f} mm"), ("Duration", f"{o['T']:.2f} s"),
            ("Baseline error", f"{b['error_mm']:.2f} mm")]
    cfg_text = json.dumps({**asdict(cfg), **{"runs": a.runs, "pop": a.pop, "iters": a.iters}}, indent=1)
    dashboard.build(a.out, table, kpis, cfg_text, p("dashboard.html"))
    report.write(p("REPORT.md"), prob, cfg, a, table, finals, times, best_name)
    print("\nDone. Open results/dashboard.html and results/REPORT.md")


if __name__ == "__main__":
    main()
