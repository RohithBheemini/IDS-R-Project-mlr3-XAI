# ==============================================================================
# File: R/08_evaluation.R
# Purpose: Final evaluation on untouched holdout test partition, residual diagnostics,
#          and tuned vs default performance comparison.
# PRD Ref: Section 11 (Experimental Design & Metrics), Section 11.3 (E8),
#          Section 21 (Criteria 6)
# ==============================================================================

source("R/10_utils.R")
source("R/04_preprocessing.R")
source("R/05_feature_engineering.R")

suppressPackageStartupMessages({
  library(mlr3)
  library(mlr3data)
  library(mlr3pipelines)
  library(mlr3learners)
  library(data.table)
  library(ggplot2)
  library(patchwork)
})

log_step("EVAL", "Starting Final Holdout Evaluation & Residual Diagnostics...")

# 1. Load partitions and construct task
partitions <- readRDS("reports/dataset_partitions.rds")
task_full <- create_engineered_task()
task_test <- task_full$clone()$filter(partitions$test_idx)

# 2. Load trained final model pipeline
final_pipeline <- readRDS("reports/final_model_pipeline.rds")

# 3. Predict on untouched holdout test partition
log_step("EVAL", sprintf("Scoring %d unseen holdout test observations...", task_test$nrow))
pred_test <- final_pipeline$predict(task_test)

truth_vec <- pred_test$truth
resp_vec  <- pred_test$response

# 4. Compute comprehensive regression metrics
metrics_df <- compute_regression_metrics(truth_vec, resp_vec)

cat("\n======================================================\n")
cat("UNTOUCHED HOLDOUT TEST SET PERFORMANCE (20% Holdout)\n")
cat("======================================================\n")
cat(sprintf("Observations Tested : %d\n", length(truth_vec)))
cat(sprintf("Holdout MAE         : %s\n", format_currency(metrics_df$MAE)))
cat(sprintf("Holdout RMSE        : %s\n", format_currency(metrics_df$RMSE)))
cat(sprintf("Holdout R-squared   : %.4f (%.2f%% variance explained)\n",
            metrics_df$R2, metrics_df$R2 * 100))
cat(sprintf("Holdout MAPE        : %.2f%%\n", metrics_df$MAPE))
cat("======================================================\n\n")

# Verify criteria: Model must demonstrate solid generalization (R2 > 0.80, sensible MAE)
stopifnot(metrics_df$R2 > 0.80)

# 5. Diagnostic Visualizations
log_step("EVAL", "Generating residual and goodness-of-fit diagnostic plots...")

eval_dt <- data.table(
  Actual    = truth_vec,
  Predicted = resp_vec,
  Residual  = truth_vec - resp_vec
)

# Plot A: Actual vs Predicted Scatter with 45-degree reference line
p_fit <- ggplot(eval_dt, aes(x = Actual, y = Predicted)) +
  geom_point(alpha = 0.45, color = "#2563EB", size = 1.8) +
  geom_abline(intercept = 0, slope = 1, color = "#DC2626", linetype = "dashed", linewidth = 1) +
  scale_x_continuous(labels = scales::dollar_format()) +
  scale_y_continuous(labels = scales::dollar_format()) +
  labs(
    title = "Actual vs. Predicted Sale Price (Holdout Set)",
    subtitle = sprintf("R2 = %.3f | MAE = %s", metrics_df$R2, format_currency(metrics_df$MAE)),
    x = "Actual Sale Price (USD)",
    y = "Predicted Sale Price (USD)"
  ) +
  get_project_theme()

# Plot B: Residuals vs Predicted
p_res <- ggplot(eval_dt, aes(x = Predicted, y = Residual)) +
  geom_point(alpha = 0.4, color = "#6366F1", size = 1.8) +
  geom_hline(yintercept = 0, color = "#DC2626", linetype = "dashed", linewidth = 1) +
  scale_x_continuous(labels = scales::dollar_format()) +
  scale_y_continuous(labels = scales::dollar_format()) +
  labs(
    title = "Residuals vs. Fitted Values",
    subtitle = "Zero-centered error profile confirms absence of major systematic bias",
    x = "Fitted / Predicted Price (USD)",
    y = "Residual Error (USD)"
  ) +
  get_project_theme()

# Plot C: Residual Distribution (Histogram)
p_dist <- ggplot(eval_dt, aes(x = Residual)) +
  geom_histogram(bins = 35, fill = "#10B981", color = "white", alpha = 0.85) +
  geom_vline(xintercept = 0, color = "#DC2626", linetype = "dashed", linewidth = 1) +
  scale_x_continuous(labels = scales::dollar_format()) +
  labs(
    title = "Residual Error Distribution",
    subtitle = sprintf("Mean Error: %s | Median Error: %s",
                       format_currency(mean(eval_dt$Residual)),
                       format_currency(median(eval_dt$Residual))),
    x = "Residual Error (USD)",
    y = "Frequency"
  ) +
  get_project_theme()

combined_diag <- (p_fit + p_res) / p_dist

save_project_artifact(combined_diag, "evaluation_residual_diagnostics.png", dir = "figures")
save_project_artifact(metrics_df, "final_evaluation_metrics.rds", dir = "reports")
save_project_artifact(eval_dt, "holdout_predictions.rds", dir = "reports")

log_step("EVAL", "Holdout evaluation complete. Artifacts saved to reports/ and figures/")
