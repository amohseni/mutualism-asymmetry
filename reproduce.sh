#!/usr/bin/env bash
# Recompute every number and figure-data file in the paper. Run from the repository root.
# The full parameter sweep (sweep.py) is the slow step; the other scripts take seconds to minutes.
set -euo pipefail
mkdir -p results/logs
cd code
for s in figure_data leverage_check alignment_checks general_checks commitment control sandbag invasion multi_ai groups elites dynamic_path monotone_params monotone_check robust_bargaining sweep analyze; do
  echo "== $s"
  python3 "$s.py" | tee "../results/logs/$s.txt"
done
cd ../paper
Rscript figures/make-figures.R   # optional: redraws the figures from paper/data (needs R; see paper/figures/FIGURES.md)
