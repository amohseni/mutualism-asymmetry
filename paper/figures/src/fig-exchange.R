# Figure 2: human payoff at agreement against AI independence, with no care.
source("figures/figstyle.R")
d <- read.csv("data/exchange.csv")
d <- subset(d, kappa == 1 & p %in% c(0.15, 0.85))
bH <- 1 - exp(-1); dH <- d$dH[1]; th_bar <- 2/3
fs <- doc$fig_pt / .pt
best <- subset(d, p == 0.15 & !is.na(best))
p <- ggplot() +
  annotate("rect", xmin = th_bar, xmax = 1, ymin = 0, ymax = 1, fill = "grey95") +
  annotate("text", x = th_bar + 0.015, y = c(0.97, 0.90), label = c("No exchange", "mutualism"),
           hjust = 0, vjust = 0.5, size = fs, colour = pal$muted) +
  annotate("segment", x = 0, xend = 1, y = bH, yend = bH, colour = pal$muted, linewidth = 0.3) +
  annotate("segment", x = 0, xend = 1, y = dH, yend = dH, colour = pal$muted, linewidth = 0.4,
           linetype = "22") +
  geom_line(data = best, aes(theta, best), colour = pal$muted, linewidth = 0.5) +
  geom_line(data = d, aes(theta, uH, linetype = factor(p)), colour = pal$accent, linewidth = 0.6) +
  scale_linetype_manual(values = c("0.15" = "solid", "0.85" = "42")) +
  annotate("text", x = 1.02, y = bH, label = "Pre-AI baseline", hjust = 0, size = fs, colour = pal$muted) +
  annotate("text", x = 1.02, y = dH, label = "If bargaining fails", hjust = 0, size = fs, colour = pal$muted) +
  annotate("text", x = 0.03, y = 0.99, label = "Most the AI would give", hjust = 0, vjust = 1,
           size = fs, colour = pal$muted) +
  annotate("text", x = 0.03, y = 0.73, label = "Weak AI bargaining power", hjust = 0, vjust = 1,
           size = fs, colour = pal$accent) +
  annotate("text", x = 0.03, y = 0.41, label = "Strong AI bargaining power", hjust = 0, vjust = 1,
           size = fs, colour = pal$accent) +
  range_frame(x = c(0, 1), y = c(0, 1)) +
  scale_x_continuous(breaks = c(0, th_bar, 1), labels = c("0", "$1 - x_h$", "1"),
                     limits = c(0, 1.32), expand = expansion(mult = c(0.01, 0))) +
  scale_y_continuous(breaks = c(0, 0.5, 1), limits = c(0, 1)) +
  labs(x = "AI independence $\\theta$", y = "Human payoff")
save_fig(p, "exchange", width = "full", aspect = 0.618)
