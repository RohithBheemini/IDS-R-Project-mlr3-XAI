# ==============================================================================
# File: R/demo_test.R
# Purpose: Comprehensive Automated End-to-End System Demo & Health Verification
# PRD Ref: Sections 5-14, 21
# ==============================================================================

suppressPackageStartupMessages({
  library(data.table)
  library(mlr3)
  library(mlr3pipelines)
  library(mlr3learners)
  library(ggplot2)
})

# Source utility helpers and feature engineering
source("R/10_utils.R")
source("R/05_feature_engineering.R")

cat("\n")
cat("======================================================================\n")
cat("     AMES HOUSING PREDICTION & EXPLAINABLE AI SYSTEM VERIFICATION     \n")
cat("                   COMPREHENSIVE END-TO-END DEMO                      \n")
cat("======================================================================\n\n")

# ------------------------------------------------------------------------------
# STEP 1: Verify All Report & Model Serialized Artifacts
# ------------------------------------------------------------------------------
cat("--- [1/6] AUDITING SERIALIZED DATA & MODEL ARTIFACTS ---\n")
required_reports <- c(
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
  "reports/project_documentation.Rmd",
  "reports/project_documentation.html"
)

all_reports_valid <- TRUE
for (rpt in required_reports) {
  if (file.exists(rpt)) {
    sz <- file.info(rpt)$size
    cat(sprintf("  ✓ %-38s [PRESENT] (%s bytes)\n", rpt, format(sz, big.mark = ",")))
  } else {
    cat(sprintf("  ✗ %-38s [MISSING]\n", rpt))
    all_reports_valid <- FALSE
  }
}
stopifnot("Missing report artifacts!" = all_reports_valid)

# ------------------------------------------------------------------------------
# STEP 2: Verify All Visualizations & Static Web Assets
# ------------------------------------------------------------------------------
cat("\n--- [2/6] AUDITING GRAPHICAL & VISUALIZATION ASSETS ---\n")
required_figures <- c(
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

all_figs_valid <- TRUE
for (fig in required_figures) {
  www_copy <- file.path("app/www", basename(fig))
  if (file.exists(fig) && file.exists(www_copy)) {
    sz <- file.info(fig)$size
    cat(sprintf("  ✓ %-42s [PRESENT & SYNCED] (%s bytes)\n", basename(fig), format(sz, big.mark = ",")))
  } else {
    cat(sprintf("  ✗ %-42s [MISSING]\n", basename(fig)))
    all_figs_valid <- FALSE
  }
}
stopifnot("Missing figure assets!" = all_figs_valid)

# ------------------------------------------------------------------------------
# STEP 3: Load Model Pipeline & Evaluate Accuracy Benchmarks
# ------------------------------------------------------------------------------
cat("\n--- [3/6] VERIFYING MODEL PERFORMANCE & HOLDOUT METRICS ---\n")
eval_metrics <- readRDS("reports/final_evaluation_metrics.rds")
pipeline <- readRDS("reports/final_model_pipeline.rds")

cat(sprintf("  - Holdout Test MAE  : %s\n", format_currency(eval_metrics$MAE)))
cat(sprintf("  - Holdout Test RMSE : %s\n", format_currency(eval_metrics$RMSE)))
cat(sprintf("  - Holdout Test R²   : %.4f (%.2f%% variance explained)\n", eval_metrics$R2, eval_metrics$R2 * 100))
cat(sprintf("  - Holdout Test MAPE : %.2f%%\n", eval_metrics$MAPE))

stopifnot("R² is below generalization threshold 0.85!" = eval_metrics$R2 > 0.85)
stopifnot("MAE is above acceptable threshold $16,000!" = eval_metrics$MAE < 16000)
cat("  ✓ Benchmark Acceptance Criteria Passed: R² > 0.85 and MAE < $16,000.\n")

# ------------------------------------------------------------------------------
# STEP 4: Live Interactive Scoring Simulation (Archetype & Edge Cases)
# ------------------------------------------------------------------------------
cat("\n--- [4/6] RUNNING PROPERTY VALUATION DEMO & EDGE CASE STRESS TESTS ---\n")
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

# Archetype 1: Starter Home
starter_home <- copy(typical_record)
starter_home[, Overall_Qual := factor("Average", levels = levels(raw_data$Overall_Qual))]
starter_home[, Gr_Liv_Area := 1050L]
starter_home[, Total_Bsmt_SF := 800L]
starter_home[, Year_Built := 1965L]
starter_home[, Year_Remod_Add := 1975L]
starter_home[, Full_Bath := 1L]
starter_home[, Half_Bath := 0L]
starter_home[, Garage_Cars := 1L]
starter_home[, Neighborhood := factor("Old_Town", levels = levels(raw_data$Neighborhood))]
starter_home <- add_engineered_features(starter_home)
pred_starter <- pipeline$predict_newdata(starter_home)$response

# Archetype 2: Median Family Home
median_home <- copy(typical_record)
median_home[, Overall_Qual := factor("Above_Average", levels = levels(raw_data$Overall_Qual))]
median_home[, Gr_Liv_Area := 1600L]
median_home[, Total_Bsmt_SF := 950L]
median_home[, Year_Built := 1995L]
median_home[, Year_Remod_Add := 2004L]
median_home[, Full_Bath := 2L]
median_home[, Half_Bath := 1L]
median_home[, Garage_Cars := 2L]
median_home[, Neighborhood := factor("College_Creek", levels = levels(raw_data$Neighborhood))]
median_home <- add_engineered_features(median_home)
pred_median <- pipeline$predict_newdata(median_home)$response

# Archetype 3: Luxury Executive Estate
luxury_estate <- copy(typical_record)
luxury_estate[, Overall_Qual := factor("Excellent", levels = levels(raw_data$Overall_Qual))]
luxury_estate[, Gr_Liv_Area := 2800L]
luxury_estate[, Total_Bsmt_SF := 1700L]
luxury_estate[, Year_Built := 2007L]
luxury_estate[, Year_Remod_Add := 2009L]
luxury_estate[, Full_Bath := 3L]
luxury_estate[, Half_Bath := 1L]
luxury_estate[, Garage_Cars := 3L]
luxury_estate[, Neighborhood := factor("Northridge_Heights", levels = levels(raw_data$Neighborhood))]
luxury_estate <- add_engineered_features(luxury_estate)
pred_luxury <- pipeline$predict_newdata(luxury_estate)$response

# Edge Case 4: Ultra Compact Cottage (400 sq ft)
cottage <- copy(starter_home)
cottage[, Gr_Liv_Area := 450L]
cottage[, Total_Bsmt_SF := 400L]
cottage <- add_engineered_features(cottage)
pred_cottage <- pipeline$predict_newdata(cottage)$response

# Edge Case 5: Mega Mansion (4,800 sq ft, 10 Rating)
mansion <- copy(luxury_estate)
mansion[, Overall_Qual := factor("Very_Excellent", levels = levels(raw_data$Overall_Qual))]
mansion[, Gr_Liv_Area := 4500L]
mansion[, Total_Bsmt_SF := 2500L]
mansion <- add_engineered_features(mansion)
pred_mansion <- pipeline$predict_newdata(mansion)$response

cat(sprintf("  1. Starter Home (1,050 sq ft, Avg Qual)      : %s\n", format_currency(pred_starter)))
cat(sprintf("  2. Median Family Home (1,600 sq ft, Abv Avg)  : %s\n", format_currency(pred_median)))
cat(sprintf("  3. Luxury Estate (2,800 sq ft, Exc Qual)     : %s\n", format_currency(pred_luxury)))
cat(sprintf("  4. Compact Cottage (450 sq ft)               : %s\n", format_currency(pred_cottage)))
cat(sprintf("  5. Mega Mansion (4,500 sq ft, Very Exc Qual) : %s\n", format_currency(pred_mansion)))

# Sanity Assertions: Monotonicity
stopifnot("Monotonicity check failed: Luxury <= Median!" = pred_luxury > pred_median)
stopifnot("Monotonicity check failed: Median <= Starter!" = pred_median > pred_starter)
stopifnot("Monotonicity check failed: Mansion <= Luxury!" = pred_mansion > pred_luxury)
stopifnot("Monotonicity check failed: Starter <= Cottage!" = pred_starter > pred_cottage)
cat("  ✓ Monotonic Economic Sanity Hierarchy Confirmed: Cottage < Starter < Median < Luxury < Mansion\n")

# ------------------------------------------------------------------------------
# STEP 5: Live Sensitivity Trajectory Grid Demo
# ------------------------------------------------------------------------------
cat("\n--- [5/6] TESTING REAL-TIME WHAT-IF MARGINAL SENSITIVITY TRAJECTORY ---\n")
test_grid_areas <- seq(1000, 3000, by = 500)
grid_dt <- rbindlist(lapply(test_grid_areas, function(a) {
  row <- copy(median_home)
  row$Gr_Liv_Area <- as.integer(a)
  row <- add_engineered_features(row)
  row
}))
grid_preds <- pipeline$predict_newdata(grid_dt)$response

for (i in seq_along(test_grid_areas)) {
  cat(sprintf("  - Living Area: %4d sq ft  -->  Estimated Valuation: %s\n", 
              test_grid_areas[i], format_currency(grid_preds[i])))
}
stopifnot("Sensitivity trajectory is not non-decreasing!" = all(diff(grid_preds) > 0))
cat("  ✓ Real-Time Marginal Valuation Trajectory Verified: strictly positive monotonic expansion.\n")

# ------------------------------------------------------------------------------
# STEP 6: Interactive Shiny Architecture & Documentation Check
# ------------------------------------------------------------------------------
cat("\n--- [6/6] SHINY APPLICATION & RMD DOCUMENTATION INTEGRITY ---\n")
stopifnot("app/app.R missing!" = file.exists("app/app.R"))
stopifnot("reports/project_documentation.Rmd missing!" = file.exists("reports/project_documentation.Rmd"))
stopifnot("reports/project_documentation.html missing!" = file.exists("reports/project_documentation.html"))

doc_html_sz <- file.info("reports/project_documentation.html")$size
cat(sprintf("  ✓ Standalone HTML Report : %s bytes (ready for browser viewing)\n", format(doc_html_sz, big.mark = ",")))
cat("  ✓ Shiny Application Files: app/app.R and app/www assets verified.\n")

cat("\n======================================================================\n")
cat("      ALL TESTS AND DEMO SCENARIOS PASSED WITH ZERO DEFECTS!           \n")
cat("======================================================================\n\n")
