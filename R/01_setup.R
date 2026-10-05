# ==============================================================================
# File: R/01_setup.R
# Purpose: Environment setup, dependency verification, canonical task loading,
#          and reproducible train/test holdout partitioning.
# PRD Ref: Section 4 (Dataset & Provenance), Section 11.2 (Validation Design)
# ==============================================================================

source("R/10_utils.R")

log_step("SETUP", "Initializing environment and verifying required packages...")

required_packages <- c(
  "mlr3",
  "mlr3data",
  "mlr3pipelines",
  "mlr3tuning",
  "mlr3learners",
  "data.table",
  "ggplot2"
)

missing_pkgs <- setdiff(required_packages, rownames(installed.packages()))
if (length(missing_pkgs) > 0) {
  stop(sprintf("The following required packages are not yet installed: %s",
               paste(missing_pkgs, collapse = ", ")))
}

suppressPackageStartupMessages({
  library(mlr3)
  library(mlr3data)
  library(mlr3pipelines)
  library(data.table)
})

# Set deterministic project seed
set_project_seed(42)

# Load canonical adapted Ames Housing task
log_step("SETUP", "Loading canonical Ames Housing task from mlr3data...")
task_ames <- tsk("ames_housing")

cat("\n======================================================\n")
cat("CANONICAL DATASET VERIFICATION SUMMARY\n")
cat("======================================================\n")
cat(sprintf("Task ID           : %s\n", task_ames$id))
cat(sprintf("Task Type         : %s\n", task_ames$task_type))
cat(sprintf("Target Variable   : %s\n", task_ames$target_names))
cat(sprintf("Total Observations: %d (Expected: 2,930)\n", task_ames$nrow))
cat(sprintf("Total Predictors  : %d (mlr3data adapted version has 81 features)\n", length(task_ames$feature_names)))
cat("======================================================\n\n")

# Verify against PRD expectations
stopifnot(task_ames$nrow == 2930)
stopifnot(length(task_ames$feature_names) %in% c(80, 81))
stopifnot(task_ames$target_names == "Sale_Price")

# Create reproducible train/holdout test split (80% train, 20% untouched holdout)
set.seed(42)
train_idx <- sample(seq_len(task_ames$nrow), size = round(0.80 * task_ames$nrow))
test_idx  <- setdiff(seq_len(task_ames$nrow), train_idx)

# Save task partition indexes for downstream scripts
partitions <- list(
  train_idx = train_idx,
  test_idx  = test_idx,
  seed      = 42,
  n_train   = length(train_idx),
  n_test    = length(test_idx)
)

save_project_artifact(partitions, "dataset_partitions.rds", dir = "reports")
log_step("SETUP", sprintf("Created partitions: %d train (80%%), %d holdout test (20%%)",
                          length(train_idx), length(test_idx)))

log_step("SETUP", "Environment setup and data verification complete.")
