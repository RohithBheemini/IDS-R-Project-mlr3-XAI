# ==============================================================================
# File: R/06_benchmark_models.R
# Purpose: Benchmark diverse regression learners on common 5-fold CV splits.
# PRD Ref: Section 10 (ML Strategy), Section 11 (Evaluation & Experiments E1-E5),
#          Section 21 (Criteria 4)
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
})

log_step("BENCHMARK", "Starting Systematic Model Benchmarking...")

# 1. Load partitions and construct training task with engineered features
partitions <- readRDS("reports/dataset_partitions.rds")
task_full <- create_engineered_task()
task_train <- task_full$clone()$filter(partitions$train_idx)

log_step("BENCHMARK", sprintf("Training task initialized with %d observations and %d features",
                              task_train$nrow, length(task_train$feature_names)))

# 2. Instantiate pipeline graphs
pipe_base  <- build_base_pipeline()
pipe_scale <- build_scaled_pipeline()

# Transparent linear baseline pipeline: minimal preprocessing on key interpretable drivers
# PRD Ref: Section 7.2 (Minimal preprocessing + linear regression for transparent reference)
pipe_linear <- po("select", selector = selector_name(c(
  "Gr_Liv_Area", "Total_Bsmt_SF", "Year_Built", "Full_Bath",
  "Total_Living_Area", "Total_Bathrooms", "Age_At_Sale", "Qual_x_LivingArea"
))) %>>%
  po("imputemedian", affect_columns = selector_type(c("integer", "numeric"))) %>>%
  po("scale")

# 3. Define candidate learners wrapped into GraphLearners
learners <- list(
  # Baseline: Predicts constant mean
  as_learner(pipe_base %>>% lrn("regr.featureless", id = "featureless")),
  # Transparent linear baseline
  as_learner(pipe_linear %>>% lrn("regr.lm", id = "linear_lm")),
  # Regularized linear model (ElasticNet / Lasso)
  as_learner(pipe_scale %>>% lrn("regr.glmnet", id = "elastic_net", s = 0.01)),
  # Single decision tree
  as_learner(pipe_base %>>% lrn("regr.rpart", id = "decision_tree", cp = 0.01)),
  # Random Forest ensemble
  as_learner(pipe_base %>>% lrn("regr.ranger", id = "random_forest", num.trees = 150, seed = 42)),
  # Gradient Boosted Trees (XGBoost)
  as_learner(pipe_base %>>% lrn("regr.xgboost", id = "xgboost", nrounds = 150, eta = 0.1, nthread = 2))
)

# Set human-readable IDs
learners[[1]]$id <- "Featureless_Baseline"
learners[[2]]$id <- "Linear_Regression"
learners[[3]]$id <- "ElasticNet_Glmnet"
learners[[4]]$id <- "Decision_Tree_Rpart"
learners[[5]]$id <- "Random_Forest_Ranger"
learners[[6]]$id <- "XGBoost"

# 4. Resampling design: 5-Fold Cross Validation instantiated once
set_project_seed(42)
cv5 <- rsmp("cv", folds = 5)
cv5$instantiate(task_train)

# 5. Define benchmark design and execute
log_step("BENCHMARK", "Constructing benchmark design on 5-fold CV across 6 candidate models...")
design <- benchmark_grid(
  tasks = task_train,
  learners = learners,
  resamplings = cv5
)

measures <- list(
  msr("regr.mae"),
  msr("regr.rmse"),
  msr("regr.rsq")
)

log_step("BENCHMARK", "Executing benchmark (this runs all 6 models across 5 folds)...")
bmr <- benchmark(design)

# 6. Aggregate results
log_step("BENCHMARK", "Aggregating benchmark performance metrics...")
bmr_scores <- bmr$score(measures)
bmr_aggregate <- bmr$aggregate(measures)

perf_table <- data.table(
  Model = bmr_aggregate$learner_id,
  MAE   = round(bmr_aggregate$regr.mae, 2),
  RMSE  = round(bmr_aggregate$regr.rmse, 2),
  R2    = round(bmr_aggregate$regr.rsq, 4)
)[order(MAE)]

cat("\n======================================================\n")
cat("BENCHMARK CROSS-VALIDATION RESULTS (5-Fold CV)\n")
cat("======================================================\n")
print(perf_table)
cat("======================================================\n\n")

# 7. Visualization: Boxplot of MAE across folds
scores_dt <- as.data.table(bmr_scores)
scores_dt[, Model := factor(learner_id, levels = perf_table$Model)]

p_bmr <- ggplot(scores_dt, aes(x = Model, y = regr.mae, fill = Model)) +
  geom_boxplot(alpha = 0.8, outlier.size = 2, show.legend = FALSE) +
  geom_jitter(width = 0.15, alpha = 0.5, size = 1.8, show.legend = FALSE) +
  coord_flip() +
  scale_y_continuous(labels = scales::dollar_format()) +
  scale_fill_brewer(palette = "Blues", direction = -1) +
  labs(
    title = "5-Fold Cross-Validation MAE Across Candidate Model Families",
    subtitle = "Tree-based ensembles (Random Forest & XGBoost) substantially outperform linear baselines",
    x = "Model Architecture",
    y = "Cross-Validation MAE (USD)"
  ) +
  get_project_theme()

save_project_artifact(p_bmr, "benchmark_01_mae_comparison.png", dir = "figures")
save_project_artifact(list(bmr = bmr, perf_table = perf_table, scores = scores_dt),
                      "benchmark_results.rds", dir = "reports")

log_step("BENCHMARK", "Benchmarking complete. Artifacts saved to reports/ and figures/")
