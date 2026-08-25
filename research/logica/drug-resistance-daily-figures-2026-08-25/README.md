# Drug-resistance daily-note figures, 2026-08-21--25

Run `python build_daily_figures.py` to recreate the PNG and PDF assets.

Data provenance:

- 2026-08-21 site counts: `ex14_scores_unfiltered_eda_report.md` in the
  `bt-loss_v4` resistance-lightweight source archive (229/29/29 residue sites;
  all 11 drug contexts retained per mutation).
- 2026-08-22: conceptual illustration only; no measured values are shown.
- 2026-08-24 cached-head values: `results/task_axis_all_baselines/REPORT.md`
  (Coelho Boltz-2 0.052, DrugCLIP 0.070; Kim Boltz-2 0.068, DrugCLIP 0.154).
- 2026-08-25 general-response values:
  `met_h2_q_transfer_cpu_v1/run/Q_TRANSFER_METRICS.json`; lower-learning-rate
  deltas: `cached_context_correct_axis_nested_v1/aggregate/summary.csv`.

The plots use an Okabe--Ito-derived colorblind-safe palette. PNGs are exported
at 300 dpi; PDFs retain vector geometry.
