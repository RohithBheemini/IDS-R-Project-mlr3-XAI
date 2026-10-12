# ==============================================================================
# File: R/07_tuning.R
# Purpose: Hyperparameter optimization using mlr3tuning with documented search
#          space, evaluation budget, and reproducible terminator.
# PRD Ref: Section 10.1 (Model Selection), Section 11.3 (Experiment E8),
#          Section 21 (Criteria 5)
# ==============================================================================

source("R/10_utils.R")
source("R/04_preprocessing.R")
source("R/05_feature_engineering.R")

suppressPackageStartupMessages({
  library(mlr3)
  library(mlr3data)
  library(mlr3pipelines)
  library(mlr3learners)
  library(mlr3tuning)
  library(mlr3misc)
  library(paradox)
  library(data.table)
  library(ggplot2)
})

log_step("TUNING", "Starting Hyperparameter Optimization for Finalist Model...")

# 1. Load training task
partitions <- readRDS("reports/dataset_partitions.rds")
task_full <- create_engineered_task()
task_train <- task_full$clone()$filter(partitions$train_idx)

# 2. Construct GraphLearner for Random Forest (Ranger)
pipe_base <- build_base_pipeline()
learner_rf <- as_learner(pipe_base %>>% lrn("regr.ranger", id = "ranger", num.trees = 150))
learner_rf$id <- "Tuned_Ranger_Pipeline"

# 3. Define hyperparameter search space using paradox
# PRD Ref: Documented search space and budget
search_space <- ps(
  ranger.mtry = p_int(lower = 15, upper = 70),
  ranger.min.node.size = p_int(lower = 2, upper = 15),
  ranger.sample.fraction = p_dbl(lower = 0.6, upper = 0.95)
)

# 4. Define tuning instance with 3-fold CV evaluation and budget terminator
set_project_seed(42)
resampling_inner <- rsmp("cv", folds = 3)
terminator <- trm("evals", n_evals = 8)

tuning_instance <- ti(
  task = task_train,
  learner = learner_rf,
  resampling = resampling_inner,
  measures = msr("regr.mae"),
  search_space = search_space,
  terminator = terminator
)

# 5. Execute optimization with random search tuner
tuner <- tnr("random_search")
log_step("TUNING", "Executing hyperparameter search (8 evaluations with 3-fold CV)...")
tuner$optimize(tuning_instance)

# 6. Extract results & best configuration
best_result <- tuning_instance$result
best_params <- tuning_instance$result_learner_param_vals

cat("\n======================================================\n")
cat("HYPERPARAMETER OPTIMIZATION SUMMARY\n")
cat("======================================================\n")
cat(sprintf("Best Cross-Validated MAE: %s\n", format_currency(best_result$regr.mae)))
cat("Optimal Hyperparameter Values:\n")
print(best_params)
cat("======================================================\n\n")

# 7. Train final tuned model on the entire training partition
log_step("TUNING", "Training final tuned pipeline on the entire 80% training dataset...")
final_pipeline <- learner_rf$clone()
final_pipeline$param_set$values <- best_params
final_pipeline$train(task_train)

# Save final pipeline and tuning artifacts
save_project_artifact(final_pipeline, "final_model_pipeline.rds", dir = "reports")
save_project_artifact(
  list(
    instance = tuning_instance,
    best_params = best_params,
    best_mae = best_result$regr.mae,
    archive = as.data.table(tuning_instance$archive)
  ),
  "tuning_results.rds",
  dir = "reports"
)

log_step("TUNING", "Final model trained and persisted to reports/final_model_pipeline.rds")
