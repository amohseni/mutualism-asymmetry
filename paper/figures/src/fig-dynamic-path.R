# Human payoff along the illustrative path, with and without selection among AI variants.
source("figures/figstyle.R")
d <- read.csv("data/dynamic_path.csv")
d$case <- factor(d$case, levels = c("No selection", "Slow", "Medium", "Fast"))
bH <- 1 - exp(-1)
lab <- c("No selection" = "No selection", "Slow" = "Slow selection", "Medium" = "Medium selection", "Fast" = "Fast selection")
d$label <- lab[as.character(d$case)]
cols <- c("No selection" = pal$muted, "Slow" = pal$accent, "Medium" = pal$accent, "Fast" = pal$accent)
ltys <- c("No selection" = "solid", "Slow" = "solid", "Medium" = "longdash", "Fast" = "dotted")
p <- ggplot(d, aes(t, uH, group = case, colour = case, linetype = case)) +
  annotate("segment", x = 0, xend = 1, y = bH, yend = bH, colour = pal$faint, linewidth = 0.3) +
  annotate("text", x = 1.02, y = bH, label = "Pre-AI baseline", hjust = 0,
           size = doc$fig_pt / .pt, colour = pal$muted) +
  geom_line(linewidth = 0.5) +
  geom_text(data = subset(d, t == 1 & case != "Fast"), aes(x = 1.02, label = label), hjust = 0,
            size = doc$fig_pt / .pt, show.legend = FALSE) +
  annotate("text", x = 0.30, y = 0.40, label = "Fast selection", hjust = 1,
           size = doc$fig_pt / .pt, colour = pal$accent) +
  scale_colour_manual(values = cols) + scale_linetype_manual(values = ltys) +
  range_frame(x = c(0, 1), y = c(0, 1)) +
  scale_x_continuous(breaks = c(0, 0.5, 1), labels = c("Now", "", "Later"),
                     expand = expansion(mult = c(0.01, 0.32))) +
  scale_y_continuous(breaks = c(0, 0.5, 1), limits = c(0, 1)) +
  labs(x = "Position on the path", y = "Human payoff")
save_fig(p, "dynamic-path", width = "full", aspect = 0.618)
