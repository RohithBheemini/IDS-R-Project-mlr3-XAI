# ==============================================================================
# File: R/10_utils.R
# Purpose: Reusable helper functions for logging, metric calculation,
#          model serialization, and custom visualization themes.
# ==============================================================================

#' Set deterministic seed across R session
#' @param seed Integer seed value (default 42)
set_project_seed <- function(seed = 42) {
  set.seed(seed)
  message(sprintf("[INFO] Random seed set to: %d", seed))
}

#' Standard console logger for pipeline steps
#' @param step Character step name or identifier
#' @param msg Character description
log_step <- function(step, msg) {
  timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  cat(sprintf("[%s] [%s] %s\n", timestamp, step, msg))
}

#' Calculate standard regression metrics on truth vs predicted vectors
#' @param truth Numeric vector of ground truth values
#' @param response Numeric vector of model predictions
#' @return A named list containing MAE, RMSE, R2, and MAPE
compute_regression_metrics <- function(truth, response) {
  residuals <- truth - response
  mae  <- mean(abs(residuals), na.rm = TRUE)
  rmse <- sqrt(mean(residuals^2, na.rm = TRUE))
  ss_tot <- sum((truth - mean(truth, na.rm = TRUE))^2, na.rm = TRUE)
  ss_res <- sum(residuals^2, na.rm = TRUE)
  r2   <- 1 - (ss_res / ss_tot)
  mape <- mean(abs(residuals / truth), na.rm = TRUE) * 100

  data.frame(
    MAE  = mae,
    RMSE = rmse,
    R2   = r2,
    MAPE = mape
  )
}

#' Format USD currency strings
#' @param x Numeric amount
#' @return Formatted character string e.g. "$180,500"
format_currency <- function(x) {
  paste0("$", format(round(x), big.mark = ",", scientific = FALSE, trim = TRUE))
}

#' Custom project ggplot2 theme
get_project_theme <- function() {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  ggplot2::theme_minimal(base_size = 11) +
    ggplot2::theme(
      plot.title = ggplot2::element_text(face = "bold", size = 13, margin = ggplot2::margin(b = 6)),
      plot.subtitle = ggplot2::element_text(color = "#555555", size = 10, margin = ggplot2::margin(b = 8)),
      axis.title = ggplot2::element_text(face = "bold", size = 10),
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major = ggplot2::element_line(color = "#E5E7EB", linewidth = 0.5),
      strip.background = ggplot2::element_rect(fill = "#F3F4F6", color = NA),
      strip.text = ggplot2::element_text(face = "bold", size = 10)
    )
}

#' Save an artifact to the reports or figures directory
#' @param object The object or plot to save
#' @param filename File name
#' @param dir Target directory (default: "reports")
save_project_artifact <- function(object, filename, dir = "reports") {
  if (!dir.exists(dir)) {
    dir.create(dir, recursive = TRUE)
  }
  filepath <- file.path(dir, filename)
  if (inherits(object, "ggplot")) {
    ggplot2::ggsave(filepath, plot = object, width = 8, height = 5, dpi = 300)
  } else {
    saveRDS(object, file = filepath)
  }
  log_step("ARTIFACT", sprintf("Saved artifact to: %s", filepath))
  invisible(filepath)
}
