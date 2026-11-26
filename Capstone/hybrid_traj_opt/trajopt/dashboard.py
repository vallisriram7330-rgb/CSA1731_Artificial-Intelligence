"""Self-contained HTML dashboard (images embedded as base64, works offline)."""
import base64, html, os


def _img(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def build(results_dir, table, kpis, cfg_text, path):
    figs = ["fig_convergence.png", "fig_bars.png", "fig_trajectories.png", "fig_torques.png",
            "fig_workspace.png", "fig_boxplot.png"]
    rows = ""
    for name, r in table.items():
        rows += (f"<tr><td>{html.escape(name)}</td><td>{r['energy']:.1f}</td><td>{r['energy_pct']:+.1f}%</td>"
                 f"<td>{r['error_mm']:.2f}</td><td>{r['jerk']:.2f}</td><td>{r['T']:.2f}</td>"
                 f"<td>{r['cost']:.4f}</td><td>{r['cost_mean']}</td><td>{r['opt_time']}</td></tr>")
    cards = "".join(f"<div class='card'><div class='v'>{v}</div><div class='l'>{html.escape(l)}</div></div>"
                    for l, v in kpis)
    imgs = "".join(f"<div class='fig'><img src='{_img(os.path.join(results_dir, f))}'></div>" for f in figs
                   if os.path.exists(os.path.join(results_dir, f)))
    page = f"""<!doctype html><html><head><meta charset='utf-8'><title>Trajectory Optimisation Dashboard</title>
<style>
body{{font-family:system-ui,Segoe UI,Arial;margin:0;background:#f3f4f6;color:#111827}}
header{{background:#111827;color:#fff;padding:18px 28px}} header h1{{margin:0;font-size:20px}}
header p{{margin:4px 0 0;color:#9ca3af;font-size:13px}}
main{{padding:20px 28px;max-width:1300px;margin:auto}}
.cards{{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:18px}}
.card{{background:#fff;border-radius:10px;padding:14px 20px;min-width:170px;box-shadow:0 1px 3px #0002}}
.card .v{{font-size:26px;font-weight:700;color:#dc2626}} .card .l{{font-size:12px;color:#6b7280}}
table{{border-collapse:collapse;width:100%;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px #0002;font-size:13px}}
th,td{{padding:8px 10px;text-align:right;border-bottom:1px solid #e5e7eb}} th:first-child,td:first-child{{text-align:left}}
th{{background:#e5e7eb}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:16px;margin-top:18px}}
.fig{{background:#fff;border-radius:10px;padding:10px;box-shadow:0 1px 3px #0002}} .fig img{{width:100%}}
pre{{background:#fff;padding:12px;border-radius:10px;font-size:12px;overflow:auto}}
</style></head><body>
<header><h1>Hybrid PSO-GWO Trajectory Optimisation – Energy-Efficient Robotic Manipulator</h1>
<p>Simulation results (measured, not assumed). Costs: lower is better.</p></header><main>
<div class='cards'>{cards}</div>
<table><tr><th>Method</th><th>Energy [J]</th><th>vs baseline</th><th>Final error [mm]</th><th>RMS jerk</th><th>Duration [s]</th>
<th>Best cost</th><th>Cost mean±std (runs)</th><th>Opt. time / run [s]</th></tr>{rows}</table>
<p style='font-size:12px;color:#6b7280'>Energy = simulated mechanical positive work + copper loss. Error = end-effector distance to target
at the end of the motion, measured on a plant with unmodelled payload and friction.</p>
<div class='grid'>{imgs}</div>
<h3>Animation</h3><div class='fig'><img src='data:image/gif;base64,{base64.b64encode(open(os.path.join(results_dir,'arm_animation.gif'),'rb').read()).decode()}' style='max-width:900px'></div>
<h3>Experiment settings</h3><pre>{html.escape(cfg_text)}</pre></main></body></html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
