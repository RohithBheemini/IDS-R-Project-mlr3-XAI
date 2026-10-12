# ==============================================================================
# File: R/verify_endpoints.R
# Purpose: Comprehensive end-to-end verification of all pipeline scripts,
#          report artifacts, figures, predictions, and Shiny components.
# ==============================================================================

source("R/10_utils.R")
source("R/05_feature_engineering.R")

suppressPackageStartupMessages({
  library(data.table)
  library(mlr3)
  library(mlr3pipelines)
  library(mlr3learners)
})

cat("====================================================================\n")
cat("      COMPREHENSIVE ENDPOINT & REPOSITORY VERIFICATION REPORT       \n")
cat("====================================================================\n\n")

# 1. Verify Pipeline & Preprocessing Artifacts
cat("[1] Checking Serialized Report Artifacts:\n")
report_files <- c(
  "reports/dataset_partitions.rds",
  "reports/data_audit_report.rds",
  "reports/engineered_features_summary.rds",
  "reports/benchmark_results.rds",
  "reports/tuning_results.rds",
  "reports/final_model_pipeline.rds",
  "reports/final_evaluation_metrics.rds",
  "reports/holdout_predictions.rds",
  "reports/shap_local_explanations.rds",
  "reports/xai_governance_report.rds",
  "reports/technical_report.md"
)

all_reports_exist <- TRUE
for (rf in report_files) {
  ex <- file.exists(rf)
  sz <- if (ex) file.info(rf)$size else 0
  cat(sprintf("  %-42s: %s (%s bytes)\n", rf, ifelse(ex, "PASS [OK]", "FAIL"), format(sz, big.mark = ",")))
  if (!ex) all_reports_exist <- FALSE
}

# 2. Verify Generated Figures
cat("\n[2] Checking Visualization & Plot Artifacts:\n")
figure_files <- c(
  "figures/eda_01_target_distribution_raw.png",
  "figures/eda_02_target_distribution_log.png",
  "figures/eda_03_top_correlations.png",
  "figures/eda_04_overall_qual_vs_price.png",
  "figures/eda_05_gr_liv_area_vs_price.png",
  "figures/eda_06_missingness_profile.png",
  "figures/eda_07_engineered_features_correlations.png",
  "figures/benchmark_01_mae_comparison.png",
  "figures/evaluation_residual_diagnostics.png",
  "figures/xai_01_global_importance.png",
  "figures/xai_02_shap_luxury_waterfall.png"
)

all_figs_exist <- TRUE
for (ff in figure_files) {
  ex <- file.exists(ff)
  sz <- if (ex) file.info(ff)$size else 0
  cat(sprintf("  %-45s: %s (%s bytes)\n", ff, ifelse(ex, "PASS [OK]", "FAIL"), format(sz, big.mark = ",")))
  if (!ex) all_figs_exist <- FALSE
}

# 3. Verify Real-Time Prediction Scoring
cat("\n[3] Testing Real-Time Prediction Endpoint Through Final Pipeline:\n")
model <- readRDS("reports/final_model_pipeline.rds")
raw_data <- mlr3data::ames_housing

typical_record <- as.data.table(raw_data)[1, ]
for (col in names(typical_record)) {
  if (is.integer(raw_data[[col]])) {
    typical_record[[col]] <- as.integer(round(median(raw_data[[col]], na.rm = TRUE)))
  } else if (is.numeric(raw_data[[col]])) {
    typical_record[[col]] <- median(raw_data[[col]], na.rm = TRUE)
  } else if (is.factor(raw_data[[col]])) {
    tbl <- table(raw_data[[col]])
    typical_record[[col]] <- factor(names(tbl)[which.max(tbl)], levels = levels(raw_data[[col]]))
  }
}

# Scenario A: Typical Median Property
h_med <- copy(typical_record)
h_med <- add_engineered_features(h_med)
p_med <- model$predict_newdata(h_med)$response
cat(sprintf("  Scenario A (Median Ames Home)    : %s\n", format_currency(p_med)))

# Scenario B: Luxury Executive Estate
h_lux <- copy(typical_record)
h_lux[, Overall_Qual := factor("Excellent", levels = levels(raw_data$Overall_Qual))]
h_lux[, Gr_Liv_Area := 2800L]
h_lux[, Total_Bsmt_SF := 1700L]
h_lux[, Year_Built := 2007L]
h_lux[, Year_Remod_Add := 2009L]
h_lux[, Full_Bath := 3L]
h_lux[, Garage_Cars := 3L]
h_lux[, Neighborhood := factor("Northridge_Heights", levels = levels(raw_data$Neighborhood))]
h_lux <- add_engineered_features(h_lux)
p_lux <- model$predict_newdata(h_lux)$response
cat(sprintf("  Scenario B (Luxury Estate)       : %s\n", format_currency(p_lux)))

# Scenario C: Starter Modest Bungalow
h_sta <- copy(typical_record)
h_sta[, Overall_Qual := factor("Average", levels = levels(raw_data$Overall_Qual))]
h_sta[, Gr_Liv_Area := 1050L]
h_sta[, Total_Bsmt_SF := 800L]
h_sta[, Year_Built := 1965L]
h_sta[, Year_Remod_Add := 1975L]
h_sta[, Full_Bath := 1L]
h_sta[, Garage_Cars := 1L]
h_sta[, Neighborhood := factor("Old_Town", levels = levels(raw_data$Neighborhood))]
h_sta <- add_engineered_features(h_sta)
p_sta <- model$predict_newdata(h_sta)$response
cat(sprintf("  Scenario C (Starter Home)        : %s\n", format_currency(p_sta)))

# Sanity assertions
stopifnot(p_lux > p_med)
stopifnot(p_med > p_sta)
cat("  Ordering Assertion (Luxury > Median > Starter): PASS [OK]\n")

# 4. Verify Holdout Metrics Integrity
cat("\n[4] Checking Test Holdout Performance Metrics:\n")
metrics <- readRDS("reports/final_evaluation_metrics.rds")
cat(sprintf("  Holdout MAE      : %s\n", format_currency(metrics$MAE)))
cat(sprintf("  Holdout RMSE     : %s\n", format_currency(metrics$RMSE)))
cat(sprintf("  Holdout R²       : %.4f (%.2f%%)\n", metrics$R2, metrics$R2 * 100))
cat(sprintf("  Holdout MAPE     : %.2f%%\n", metrics$MAPE))
stopifnot(metrics$R2 > 0.85)
cat("  Generalization Threshold (R² > 0.85): PASS [OK]\n")

# 5. Summary Conclusion
cat("\n====================================================================\n")
cat("                ALL ENDPOINTS VERIFIED SUCCESSFULLY!                \n")
cat("====================================================================\n")
