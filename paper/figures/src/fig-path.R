# Figure 1: human payoff and the required degree of alignment along the illustrative path.
source("figures/figstyle.R")
library(patchwork)
d <- read.csv("data/path.csv")
bH <- d$bH[1]
t_end <- min(d$t[d$uH <= bH])               # exchange mutualism ends here
fs <- doc$fig_pt / .pt
xsc <- scale_x_continuous(breaks = c(0, 0.5, 1), labels = c("Now", "", "Later"),
                          limits = c(0, 1.32), expand = expansion(mult = c(0.01, 0)))
vline <- annotate("segment", x = t_end, xend = t_end, y = 0, yend = 1,
                  colour = pal$faint, linewidth = 0.3)

top <- ggplot(d, aes(t)) +
  vline +
  annotate("text", x = t_end + 0.015, y = 1, label = "Exchange mutualism ends",
           hjust = 0, vjust = 1, size = fs, colour = pal$muted) +
  geom_line(aes(y = bH), colour = pal$muted, linewidth = 0.3) +
  geom_line(aes(y = dH), colour = pal$muted, linewidth = 0.4, linetype = "22") +
  geom_line(aes(y = uH), colour = pal$accent, linewidth = 0.6) +
  annotate("text", x = 1.02, y = bH, label = "Pre-AI baseline", hjust = 0, size = fs, colour = pal$muted) +
  annotate("text", x = 1.02, y = d$dH[nrow(d)], label = "If bargaining fails", hjust = 0, vjust = 0.2,
           size = fs, colour = pal$muted) +
  annotate("text", x = 0.62, y = 0.43, label = "Agreement, no care", hjust = 0, size = fs,
           colour = pal$accent) +
  range_frame(y = c(0, 1)) + xsc +
  scale_y_continuous(breaks = c(0, 0.5, 1), limits = c(0, 1)) +
  labs(x = NULL, y = "Human payoff") +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank())

bot <- ggplot(d, aes(t, alpha_star)) +
  vline +
  geom_line(colour = pal$accent, linewidth = 0.6) +
  annotate("text", x = 1.02, y = c(1, 0.89), label = c("Required degree", "of alignment"),
           hjust = 0, vjust = 0.5, size = fs, colour = pal$accent) +
  range_frame(x = c(0, 1), y = c(0, 1)) + xsc +
  scale_y_continuous(breaks = c(0, 0.5, 1), limits = c(0, 1)) +
  labs(x = "Position on the path", y = "$\\alpha^*$")

p <- top / bot + plot_layout(heights = c(1, 0.8))
save_fig(p, "path", width = "full", height = 3.9)
