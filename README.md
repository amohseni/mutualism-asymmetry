# Human–AI Mutualism Is Unstable under Capability Asymmetry

Aydin Mohseni, Carnegie Mellon University. November 2026.

**Paper:** [paper/mutualism-asymmetry.pdf](paper/mutualism-asymmetry.pdf)

One hope for a good human future alongside advanced AI rests on enduring mutualism: humans and AI will need each other, so the relationship will stay good for both. The paper argues that this hope fails as AI capability grows. In a simple bargaining model, humans stay as well off as before AI without alignment only while they have leverage over the AI: either the AI depends on what they supply, or they can impose costs on the AI that are large relative to what the AI can produce. Once humans have neither kind of leverage, they stay as well off as before AI only if the AI is aligned with them, and if the AI's goals are insatiable, the alignment required approaches perfect alignment as AI capability grows. Mutualism is therefore not a substitute for alignment.

This repository holds the paper, its LaTeX source, and the code and data behind every number and figure in it.

## Contents

| Folder | What it holds |
|---|---|
| `paper/` | LaTeX source, bibliography, compiled PDF, figure data (`data/`) and figure scripts (`figures/`) |
| `code/` | Python scripts, one per result (table below) |
| `results/` | Saved outputs: JSON results and the full parameter sweep (`sweep_manifest.json`) |
| `results/logs/` | Printed output of each script from the last full run |

## Which script supports which result

Proofs of all propositions and the theorem are in Appendix B of the paper. The scripts compute the numerical examples and check the analytic results. Appendix A of the paper ("Extensions") holds Remarks 9 and 10, Propositions 11 to 13, and Results 1 and 2.

| Paper | Script | Output |
|---|---|---|
| Figure 1, illustrative path (§3); Figure 2, Propositions 1(i) and 2 | `figure_data.py` (solver in `model.py`) | `paper/data/path.csv`, `paper/data/exchange.csv` |
| Proposition 1(ii) (cost of conflict for the AI) | `leverage_check.py` | log |
| End of exchange mutualism on the path; tightness of Proposition 3(i) | `alignment_checks.py` | log |
| Robustness of Propositions 1 and 3(ii) to nonlinear goal output (not reported in the paper) | `general_checks.py` | log |
| Theorem 4 (monotonicity) | `monotone_params.py` | log |
| Proposition 5 (commitment) and Proposition 12 (commitment and alignment), with the example in Appendix C | `commitment.py` | `commitment_results.json` |
| Proposition 6 (sandbagging) | `sandbag.py` | `sandbag_results.json` |
| Proposition 7 (invasion) | `invasion.py` | log |
| Proposition 8 (chokepoints), competing elites | `elites.py` | `elites_results.json` |
| Remark 9 (competition among AIs), Proposition 13 (care as a public good) | `multi_ai.py` | `multi_ai_results.json` |
| Proposition 11 (control) | `control.py` | `control_results.json` |
| Result 1 and Figure 3 (selection along the path) | `dynamic_path.py` | `dynamic_path.json`, `paper/data/dynamic_path.csv` |
| Result 2 (several human groups) | `groups.py` | `groups_results.json` |
| Appendix C: sweep, regimes, sensitivity | `sweep.py`, `analyze.py` | `sweep_manifest.json` |
| Appendix C: other bargaining solutions | `robust_bargaining.py` | log |
| Appendix C: the required degree of alignment is a threshold | `monotone_check.py` | log |

## Reproducing the results

```bash
pip install -r requirements.txt
./reproduce.sh          # runs every script from code/ and writes results/ and paper/data/
```

The full sweep (32,768 model solutions) takes a few minutes on four cores. The figures are drawn in R with ggplot2 and tikzDevice from the CSV files in `paper/data/`; `paper/figures/FIGURES.md` lists the packages and settings. To compile the paper:

```bash
cd paper && ./build.sh
```

## Notation in the code

The scripts were written before the paper's notation settled. Where they differ:

- `alpha`, `kappa`, `theta`, `delta`, `p`, `xbar`, `s` are α, κ, θ, δ, p, x̄, s in the paper.
- In `sweep.py`, `norm=False` is the convention in which goal value scales with capability; `norm=True` is the convention in which it does not (Appendix C).
- In `sandbag.py`, `h`, `e` and `sig` are μ (probability of high capability), η (detection probability) and ζ (hiding cost) in Proposition 6.
- In `control.py`, the "satiable" goal is the bounded goal of Proposition 11.

## Citation

See `CITATION.cff`, or cite as:

> Mohseni, Aydin. 2026. "Human–AI Mutualism Is Unstable under Capability Asymmetry." Working paper.

## License

Code: MIT (`LICENSE`). Paper: CC BY 4.0 (`LICENSE-paper.md`).
