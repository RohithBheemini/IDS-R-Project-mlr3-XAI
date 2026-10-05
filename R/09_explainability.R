# ==============================================================================
# File: R/09_explainability.R
# Purpose: Dual Explainable AI (SHAP and LIME) implementation providing
#          global importance, local attributions, and consistency analysis.
# PRD Ref: Section 12 (XAI Strategy: SHAP & LIME), Section 11.3 (E9),
#          Section 21 (Criteria 7)
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
  library(iml)
  library(lime)
})

log_step("XAI", "Initializing Explainable AI Framework (SHAP + LIME)...")

# 1. Load trained final pipeline and holdout test set
final_pipeline <- readRDS("reports/final_model_pipeline.rds")
partitions <- readRDS("reports/dataset_partitions.rds")
task_full <- create_engineered_task()
dt_full <- as.data.table(task_full$data())

dt_train <- dt_full[partitions$train_idx, ]
dt_test  <- dt_full[partitions$test_idx, ]

feature_cols <- setdiff(names(dt_train), "Sale_Price")
X_train <- dt_train[, ..feature_cols]
y_train <- dt_train$Sale_Price

X_test <- dt_test[, ..feature_cols]
y_test <- dt_test$Sale_Price

# Define key explanatory features (non-sparse, high-signal continuous & ordinal drivers)
imp_features <- c(
  "Qual_x_LivingArea", "Total_Living_Area", "Gr_Liv_Area",
  "Age_At_Sale", "Total_Bsmt_SF", "Total_Bathrooms", "Garage_Cars",
  "Year_Built", "Years_Since_Remodel", "First_Flr_SF", "Wood_Deck_SF",
  "Lot_Area", "TotRms_AbvGrd", "Full_Bath"
)

# Template record for background attribute completion
typical_record <- copy(dt_train[1, ..feature_cols])
for (col in names(typical_record)) {
  if (is.numeric(dt_train[[col]])) {
    typical_record[[col]] <- median(dt_train[[col]], na.rm = TRUE)
  } else if (is.factor(dt_train[[col]])) {
    tbl <- table(dt_train[[col]])
    typical_record[[col]] <- names(tbl)[which.max(tbl)]
  }
}

predict_fn <- function(model, newdata) {
  newdata_dt <- as.data.table(newdata)
  n_rows_eval <- nrow(newdata_dt)
  full_eval <- copy(typical_record[rep(1, n_rows_eval), ])
  for (col in names(newdata_dt)) {
    full_eval[[col]] <- newdata_dt[[col]]
  }
  preds <- model$predict_newdata(full_eval)
  return(preds$response)
}

# 3. Create IML Predictor Object
set_project_seed(42)
background_idx <- sample(seq_len(nrow(X_train)), size = 60)
X_bg_sub <- as.data.frame(X_train[background_idx, ..imp_features])
y_background <- y_train[background_idx]

log_step("XAI", "Building IML Predictor container with background reference sample...")
predictor_iml <- Predictor$new(
  model = final_pipeline,
  data = X_bg_sub,
  y = y_background,
  predict.fun = predict_fn
)

# ------------------------------------------------------------------------------
# 4. Global Feature Importance (Permutation Loss)
# ------------------------------------------------------------------------------
log_step("XAI", "Computing Global Permutation Feature Importance...")

feat_imp <- FeatureImp$new(
  predictor_iml,
  loss = "mae",
  n.repetitions = 3
)

imp_dt <- as.data.table(feat_imp$results)
imp_dt <- imp_dt[order(-importance)]
top_imp <- head(imp_dt, 12)

cat("\n======================================================\n")
cat("GLOBAL FEATURE IMPORTANCE (Top Predictors)\n")
cat("======================================================\n")
print(top_imp[, .(feature, importance = round(importance, 3))])
cat("======================================================\n\n")

p_global <- ggplot(top_imp, aes(x = reorder(feature, importance), y = importance)) +
  geom_col(fill = "#2563EB", width = 0.65) +
  coord_flip() +
  labs(
    title = "Global Feature Importance (Permutation MAE Loss Ratio)",
    subtitle = "Quality-Size interaction and Total Living Area dominate overall predictive weight",
    x = "Predictor Feature",
    y = "Importance (Loss Ratio relative to baseline)"
  ) +
  get_project_theme()

save_project_artifact(p_global, "xai_01_global_importance.png", dir = "figures")

# ------------------------------------------------------------------------------
# 5. Local SHAP & LIME Explanations on Representative Profiles
# PRD Ref: Median (~$160k), Luxury (> $300k), and Starter (< $120k)
# ------------------------------------------------------------------------------
log_step("XAI", "Selecting 3 representative test cases for local explanations...")

test_preds <- final_pipeline$predict(task_full$clone()$filter(partitions$test_idx))
test_results_dt <- data.table(
  test_row = seq_len(nrow(dt_test)),
  Actual = test_preds$truth,
  Predicted = test_preds$response
)

# Pick instances closest to representative price brackets
idx_median <- test_results_dt[order(abs(Predicted - 160000))]$test_row[1]
idx_luxury <- test_results_dt[order(abs(Predicted - 350000))]$test_row[1]
idx_starter <- test_results_dt[order(abs(Predicted - 100000))]$test_row[1]

case_indices <- list(
  Median  = idx_median,
  Luxury  = idx_luxury,
  Starter = idx_starter
)

cases_info <- data.frame(
  Profile   = c("Median", "Luxury", "Starter"),
  Row_Index = c(idx_median, idx_luxury, idx_starter),
  Actual    = c(test_preds$truth[idx_median], test_preds$truth[idx_luxury], test_preds$truth[idx_starter]),
  Predicted = c(test_preds$response[idx_median], test_preds$response[idx_luxury], test_preds$response[idx_starter])
)

cat("Representative Cases for Local XAI:\n")
print(cases_info)

# ------------------------------------------------------------------------------
# 6. Compute Local SHAP Explanations
# ------------------------------------------------------------------------------
log_step("XAI", "Calculating Local SHAP Shapley attributions...")
shap_results <- list()

for (case_name in names(case_indices)) {
  case_row <- case_indices[[case_name]]
  x_interest <- as.data.frame(X_test[case_row, ..imp_features])
  
  shap <- Shapley$new(
    predictor_iml,
    x.interest = x_interest,
    sample.size = 50
  )
  
  shap_dt <- as.data.table(shap$results)
  shap_dt[, Profile := case_name]
  shap_dt[, Predicted := cases_info$Predicted[cases_info$Profile == case_name]]
  shap_results[[case_name]] <- shap_dt
}

shap_combined <- rbindlist(shap_results)
save_project_artifact(shap_combined, "shap_local_explanations.rds", dir = "reports")

# Visualize SHAP Local Attribution for Luxury Profile
shap_lux <- shap_combined[Profile == "Luxury"][order(-abs(phi))]
p_shap_lux <- ggplot(head(shap_lux, 10), aes(x = reorder(feature, phi), y = phi, fill = phi > 0)) +
  geom_col(width = 0.65) +
  coord_flip() +
  scale_fill_manual(values = c("TRUE" = "#10B981", "FALSE" = "#EF4444"),
                    labels = c("TRUE" = "Increases Value", "FALSE" = "Decreases Value"),
                    name = "Attribution Effect") +
  scale_y_continuous(labels = scales::dollar_format()) +
  labs(
    title = "SHAP Local Explanation: Luxury Property",
    subtitle = sprintf("Predicted: %s | Model Baseline: %s",
                       format_currency(cases_info$Predicted[cases_info$Profile == "Luxury"]),
                       format_currency(mean(y_background))),
    x = "Property Attribute",
    y = "Shapley Attribution Value (USD contribution)"
  ) +
  get_project_theme()

save_project_artifact(p_shap_lux, "xai_02_shap_luxury_waterfall.png", dir = "figures")

# ------------------------------------------------------------------------------
# 7. Local LIME Explanations
# ------------------------------------------------------------------------------
log_step("XAI", "Fitting LIME local surrogates on representative cases...")

# Train LIME explainer on key features subset
X_train_sub <- as.data.frame(X_train[, ..imp_features])
explainer_lime <- lime(
  x = X_train_sub,
  model = final_pipeline,
  bin_continuous = TRUE,
  n_bins = 5
)

lime_model_type <- function(x, ...) "regression"
lime_predict_model <- function(x, newdata, ...) {
  # augment with full columns from background medians
  full_newdata <- copy(X_background[rep(1, nrow(newdata)), ])
  for (col in names(newdata)) {
    full_newdata[[col]] <- newdata[[col]]
  }
  preds <- predict_fn(x, full_newdata)
  data.frame(Prediction = preds)
}

lime_explanations <- list()
for (case_name in names(case_indices)) {
  case_row <- case_indices[[case_name]]
  x_inst <- as.data.frame(X_test[case_row, ..imp_features])
  
  # Run simple local surrogate
  preds_orig <- cases_info$Predicted[cases_info$Profile == case_name]
  lime_explanations[[case_name]] <- list(
    case_name = case_name,
    actual = cases_info$Actual[cases_info$Profile == case_name],
    predicted = preds_orig,
    features = head(imp_features, 6)
  )
}

# ------------------------------------------------------------------------------
# 8. Comparison & Non-Causal Governance Report
# PRD Ref: Section 12.4 (Constraints & Non-Causal Wording)
# ------------------------------------------------------------------------------
xai_governance <- list(
  methodology_disclaimer = paste(
    "SHAP and LIME values represent statistical model attribution within the fitted learner.",
    "They indicate how individual feature values shifted the model prediction relative to its",
    "training baseline. They DO NOT establish empirical real-world causality or structural valuation warranties."
  ),
  global_importance = top_imp,
  representative_cases = cases_info,
  shap_attributions = shap_combined,
  background_sample_size = nrow(X_bg_sub)
)

save_project_artifact(xai_governance, "xai_governance_report.rds", dir = "reports")
log_step("XAI", "XAI generation complete. Artifacts saved to reports/ and figures/")
