# figstyle.R: shared figure style for one document.
# Copy into <document>/figures/, edit the DOCUMENT block, and source() it from
# every figure script. Everything a figure needs to match its siblings lives here.

suppressPackageStartupMessages({
  library(ggplot2)
})

# ---- DOCUMENT: edit once per document -------------------------------------
doc <- list(
  class      = "amsart",   # "amsart", "article", or "tufte"
  textwidth  = 5.35,       # measured with \typeout{\the\textwidth}; inches
  body_pt    = 11,         # body font size
  fig_pt     = 9,          # tick-label size at print; axis titles fig_pt + 1
  font       = "cm",       # "cm" (Computer Modern via tikzDevice) or a cairo family name
  preamble   = NULL        # path to a .tex with \usepackage lines tikzDevice should load
)

# Slot widths in inches, derived from the document block.
slot <- list(
  full  = doc$textwidth,
  half  = (doc$textwidth - 0.25) / 2,
  third = (doc$textwidth - 0.5) / 3
)
if (doc$class == "tufte") {
  slot <- list(full = 4.33, margin = 2.0, fullwidth = 6.5, half = 2.05)
}

# ---- Palette ---------------------------------------------------------------
# One emphasis color, greys for context. Category-to-color mapping is fixed per
# document: set it in `pal$map` and use scale_color_doc() so it never drifts.
pal <- list(
  ink      = "grey15",
  muted    = "grey55",
  faint    = "grey80",
  accent   = "#1f5fa8",   # emphasis
  accent2  = "#c9532b",   # only for a two-way contrast
  cat      = c("#1f5fa8", "#c9532b", "#4a8a3c", "#8b5fb8", "#b8860b"),  # at most five
  map      = c()          # e.g. c("baseline" = "grey55", "treatment" = "#1f5fa8")
)

scale_color_doc <- function(...) {
  if (length(pal$map)) scale_color_manual(values = pal$map, ...) else
    scale_color_manual(values = pal$cat, ...)
}
scale_fill_doc <- function(...) {
  if (length(pal$map)) scale_fill_manual(values = pal$map, ...) else
    scale_fill_manual(values = pal$cat, ...)
}

# ---- Theme -----------------------------------------------------------------
theme_paper <- function(base_size = doc$fig_pt, base_family = "") {
  half_line <- base_size / 2
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      line = element_line(colour = pal$ink, linewidth = 0.3, lineend = "butt"),
      text = element_text(colour = pal$ink, size = base_size),
      panel.grid = element_blank(),
      panel.background = element_blank(),
      panel.border = element_blank(),
      plot.background = element_blank(),
      axis.line = element_blank(),        # range_frame() draws the axes
      axis.ticks = element_line(colour = pal$ink, linewidth = 0.3),
      axis.ticks.length = unit(half_line / 2, "pt"),
      axis.text = element_text(colour = pal$ink, size = base_size),
      axis.title = element_text(size = base_size + 1),
      axis.title.y = element_text(angle = 90, margin = margin(r = half_line)),
      axis.title.x = element_text(margin = margin(t = half_line)),
      strip.text = element_text(size = base_size, hjust = 0,
                                margin = margin(b = half_line / 2)),
      strip.background = element_blank(),
      legend.position = "none",           # direct labels by default
      legend.background = element_blank(),
      legend.key = element_blank(),
      legend.title = element_blank(),
      plot.title = element_blank(),       # the caption is the title
      plot.margin = margin(2, 6, 2, 2),   # right margin leaves room for end labels
      complete = TRUE
    )
}

# Range frame: axis segments spanning the data range only (Tufte).
# Add to a plot; pass the data used for the axes if it differs from the plot's.
range_frame <- function(data = NULL, x = NULL, y = NULL, colour = pal$ink) {
  list(
    if (!is.null(x)) annotate("segment", x = min(x), xend = max(x),
                              y = -Inf, yend = -Inf, colour = colour, linewidth = 0.3),
    if (!is.null(y)) annotate("segment", x = -Inf, xend = -Inf,
                              y = min(y), yend = max(y), colour = colour, linewidth = 0.3)
  )
}
# Plain full axes, for the exceptions in tufte-rules.md.
plain_axes <- function() theme(axis.line = element_line(colour = pal$ink, linewidth = 0.3))

# ---- Direct labels ---------------------------------------------------------
# Label each series at its right end. `data` must be the plot data; `group`
# the series column; `label` the text column (defaults to group).
end_labels <- function(data, x, y, group, label = group, nudge = 0.02) {
  requireNamespace("ggrepel")
  x <- rlang::ensym(x); y <- rlang::ensym(y); group <- rlang::ensym(group)
  label <- rlang::ensym(label)
  ends <- data |>
    dplyr::group_by(!!group) |>
    dplyr::slice_max(!!x, n = 1, with_ties = FALSE) |>
    dplyr::ungroup()
  xr <- range(dplyr::pull(data, !!x))
  ggrepel::geom_text_repel(
    data = ends, aes(x = !!x, y = !!y, label = !!label),
    hjust = 0, direction = "y", nudge_x = nudge * diff(xr),
    segment.colour = NA, size = doc$fig_pt / .pt, seed = 1,
    min.segment.length = Inf, box.padding = 0.1
  )
}

# ---- Saving ----------------------------------------------------------------
# Save at final physical size. Prefer tikzDevice so LaTeX sets the text in the
# document font; fall back to cairo_pdf with an explicit family.
# width: a slot name ("full", "half", "margin", ...) or inches.
save_fig <- function(plot, slug, width = "full", aspect = 0.618, height = NULL,
                     dir = "figures", engine = c("tikz", "cairo")) {
  engine <- match.arg(engine)
  w <- if (is.character(width)) slot[[width]] else width
  h <- if (is.null(height)) w * aspect else height
  stopifnot(!is.null(w))
  dir.create(dir, showWarnings = FALSE, recursive = TRUE)
  out <- file.path(dir, paste0("fig-", slug, ".pdf"))
  if (engine == "tikz" && requireNamespace("tikzDevice", quietly = TRUE)) {
    tex <- file.path(dir, paste0("fig-", slug, ".tex"))
    opts <- list(tikzDocumentDeclaration = "\\documentclass[11pt]{article}")
    if (!is.null(doc$preamble))
      opts$tikzLatexPackages <- c(getOption("tikzLatexPackages"),
                                  paste0("\\input{", normalizePath(doc$preamble), "}"))
    old <- options(opts)
    on.exit(options(old), add = TRUE)
    tikzDevice::tikz(tex, width = w, height = h, standAlone = TRUE, sanitize = FALSE)
    print(plot)
    dev.off()
    owd <- setwd(dir); on.exit(setwd(owd), add = TRUE)
    system2("pdflatex", c("-interaction=batchmode", "-halt-on-error", basename(tex)),
            stdout = FALSE)
    file.remove(list.files(dir, pattern = paste0("^fig-", slug, "\\.(aux|log)$"),
                           full.names = TRUE))
  } else {
    family <- if (doc$font == "cm") "CMU Serif" else doc$font
    ggsave(out, plot, device = cairo_pdf, width = w, height = h, units = "in",
           family = family)
  }
  message("wrote ", out, "  (", round(w, 2), " x ", round(h, 2), " in)")
  invisible(out)
}

theme_set(theme_paper())
