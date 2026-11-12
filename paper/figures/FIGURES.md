# Figures registry

Document class: amsart (canonical preamble)
Text width: 5.35 in (measured 2026-10-13: 386.67 pt)
Figure text size: 9 pt (doc$fig_pt; TikZ \small)
Engine: tikzDevice (ggplot2) / standalone pdflatex (TikZ)
Palette mapping (category -> color): no selection = muted grey; selection cases = accent blue, line type by speed (solid slow, long dash medium, dotted fast)
Families: path (x = position on the path, Now to Later; y = human payoff 0 to 1; aspect 0.618)

| slug | source | tool | slot | family | aspect | status |
|---|---|---|---|---|---|---|
| dynamic-path | src/fig-dynamic-path.R (data/dynamic_path.csv from stage6/dynamic_path.py) | ggplot2 + tikzDevice | full | path | 0.618 | v0.1, inspected on page |
| path | src/fig-path.R (data/path.csv from stage7/figure_data.py) | ggplot2 + patchwork + tikzDevice | full | path | 3.9 in tall, two panels | v0.1, inspected on page (Figure 1) |
| exchange | src/fig-exchange.R (data/exchange.csv from stage7/figure_data.py) | ggplot2 + tikzDevice | full | single | 0.618 | v0.1, inspected on page (Figure 2) |

Placement: all figures [tp]; float pages top-aligned (\@fptop = 0pt). Palette: agreement curves accent blue; baselines and bargaining-failure lines grey (dashed for bargaining failure); shaded grey95 = region with no exchange mutualism.
