# Hybrid AI-Based Trajectory Optimization for Energy-Efficient Robotic Manipulator Control using PSO and GWO

A complete, runnable Python project that

1. simulates a 2-DOF robotic arm with full rigid-body dynamics, a computed-torque + PID controller,
   torque saturation, and a deliberately *imperfect* controller model (unmodelled payload + friction);
2. optimises the arm's joint trajectory with **PSO**, **GWO** and a **Hybrid PSO-GWO**;
3. compares them with a standard (quintic) baseline on **energy, positioning error, smoothness and duration**;
4. produces graphs, an animation, an HTML dashboard and an auto-generated report.

## Quick start

```bash
pip install -r requirements.txt     # numpy, matplotlib, pillow
python main.py --quick              # smoke test, about 1-2 minutes
python main.py                      # full experiment: 10 runs x 3 algorithms (about 10-15 min on one CPU core)
```

Then open `results/dashboard.html` (works offline) and `results/REPORT.md`.

Options: `--runs 10 --pop 30 --iters 60 --seed 0 --out results`

## Project layout

```
main.py                  run everything, write all outputs
trajopt/robot.py         2-link arm: kinematics, inverse/forward dynamics
trajopt/trajectory.py    trajectory parameterisation (quintic + shape functions + duration T)
trajopt/fitness.py       simulation (plant + controller), metrics, cost function, all settings
trajopt/optimizers.py    PSO, GWO, Hybrid PSO-GWO (same budget, same initial population per seed)
trajopt/visualize.py     plots + robot-arm animation
trajopt/dashboard.py     HTML dashboard
trajopt/report.py        report generator (numbers are filled in from the actual run)
results/                 outputs of the run included in this ZIP
```

## Features -> where they live

| Feature | Implementation |
|---|---|
| AI-based trajectory optimisation | `optimizers.py`, 7 decision variables (path shape + duration) |
| Energy reduction | `fitness.py`: E = integral of [max(tau*w,0) + R*tau^2] dt, measured in simulation |
| Hybrid PSO-GWO | `optimizers.hybrid_pso_gwo` |
| Smooth movement | RMS jerk in the cost; zero velocity/acceleration at both ends by construction |
| Positioning accuracy | end-effector error at the end of the motion, measured on the plant |
| Joint constraints | angle / velocity / acceleration / torque limits, penalty in the cost |
| Robot arm simulation | `visualize.animate` -> `results/arm_animation.gif` |
| Performance comparison | `results/comparison_table.csv`, `fig_bars.png`, `fig_boxplot.png` |
| Dashboard | `results/dashboard.html` |

## Things to change for your own experiments

All in `trajopt/fitness.py -> Settings`: start/goal joint angles, limits, cost weights `w`
(energy, accuracy, smoothness, time), controller gains, payload mismatch, energy-model coefficient `R_loss`.

## Honest notes

* Everything is **simulation**; the energy figure is a model-based estimate, not a hardware measurement.
* The optimised trajectories are mostly *faster* than the 3 s baseline. The report therefore also includes a
  **matched-duration baseline** so that saving from "moving faster" is separated from saving due to a better path shape.
* Differences between PSO, GWO and the hybrid are small compared with run-to-run variation; the report states
  this explicitly. Use more runs (`--runs 30`) before drawing strong conclusions.
* A first version of the simulator was numerically unstable for slow motions (it inflated the baseline's energy).
  This was found and fixed (finer time step + sub-stepping, checked against a 3x finer reference simulation).
