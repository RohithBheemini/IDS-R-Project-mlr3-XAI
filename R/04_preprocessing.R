# ==============================================================================
# File: R/04_preprocessing.R
# Purpose: Define and validate leakage-safe mlr3pipelines preprocessing DAGs.
# PRD Ref: Section 7 (Solution Architecture), Section 8 (Preprocessing Plan),
#          Section 15.3 (mlr3pipelines paper), Section 21 (Criteria 3)
# ==============================================================================

if (!exists("log_step")) {
  source(if (file.exists("R/10_utils.R")) "R/10_utils.R" else if (file.exists("../R/10_utils.R")) "../R/10_utils.R" else "10_utils.R")
}

suppressPackageStartupMessages({
  library(mlr3)
  library(mlr3pipelines)
  library(data.table)
})

log_step("PREPROC", "Defining mlr3pipelines Preprocessing Graphs...")

#' Construct the standard leakage-safe preprocessing pipeline
#' Addresses constant features, duplicates, redundant scales, imputation, and encoding.
#' @param target_levels Maximum factor levels to keep before collapsing rare categories (default 15)
#' @return An mlr3pipelines Graph object
build_base_pipeline <- function(target_levels = 15) {
  # 1. PipeOpRemoveConstants: drops constant features like 'Misc_Feature_2'
  po_const <- po("removeconstants", id = "remove_constants")

  # 2. PipeOpSelect: drop exact duplicates ('Condition_3') and duplicate scales ('Lot_Area_m2')
  po_select <- po(
    "select",
    id = "remove_duplicates",
    selector = selector_invert(selector_name(c("Condition_3", "Lot_Area_m2")))
  )

  # 3. Numeric imputation: median imputation learned strictly on training fold
  po_imp_num <- po(
    "imputemedian",
    id = "impute_numeric",
    affect_columns = selector_type(c("integer", "numeric"))
  )

  # 4. Factor imputation: explicit 'MISSING' out-of-range level preserving missing semantics
  po_imp_fct <- po(
    "imputeoor",
    id = "impute_factor",
    affect_columns = selector_type("factor")
  )

  # 5. Factor collapsing: collapse rare levels to maintain stability across resampling folds
  po_collapse <- po(
    "collapsefactors",
    id = "collapse_factors",
    target_level_count = target_levels
  )

  # 6. One-hot / Treatment encoding for model families requiring numeric design matrices
  po_encode <- po(
    "encode",
    id = "encode_factors",
    method = "treatment"
  )

  # 7. Post-encode zero-imputer: guarantees 0 for any unseen test factor dummy columns
  po_post_imp <- po(
    "imputeconstant",
    id = "post_encode_impute",
    constant = 0
  )

  # Compose DAG sequentially
  pipe <- po_const %>>%
    po_select %>>%
    po_imp_num %>>%
    po_imp_fct %>>%
    po_collapse %>>%
    po_encode %>>%
    po_post_imp

  return(pipe)
}

#' Construct scaled preprocessing pipeline for regularized/linear models
#' @return mlr3pipelines Graph object with centering and scaling
build_scaled_pipeline <- function(target_levels = 15) {
  base_pipe <- build_base_pipeline(target_levels = target_levels)
  po_scale <- po("scale", id = "standardize_features")
  return(base_pipe %>>% po_scale)
}

# ------------------------------------------------------------------------------
# Validation & Smoke Test on Ames Task
# ------------------------------------------------------------------------------
if (sys.nframe() == 0) {
  log_step("PREPROC", "Validating Preprocessing Pipeline Graph on Ames task...")
  library(mlr3data)
  
  task <- tsk("ames_housing")
  pipe <- build_base_pipeline()
  
  # Train pipeline graph on task
  log_step("PREPROC", "Training pipeline graph to verify state tracking...")
  processed_task <- pipe$clone()$train(task)[[1]]
  
  cat("\n======================================================\n")
  cat("PREPROCESSING PIPELINE VALIDATION\n")
  cat("======================================================\n")
  cat(sprintf("Original Task Features : %d\n", length(task$feature_names)))
  cat(sprintf("Processed Task Features: %d\n", length(processed_task$feature_names)))
  cat(sprintf("Constant Feature 'Misc_Feature_2' Present? %s\n",
              "Misc_Feature_2" %in% processed_task$feature_names))
  cat(sprintf("Duplicate Feature 'Condition_3' Present? %s\n",
              "Condition_3" %in% processed_task$feature_names))
  cat(sprintf("Duplicate Scale 'Lot_Area_m2' Present? %s\n",
              "Lot_Area_m2" %in% processed_task$feature_names))
  cat(sprintf("Any Missing Values Remaining in Processed Task? %s\n",
              any(processed_task$missings() > 0)))
  cat("======================================================\n\n")
  
  stopifnot(!"Misc_Feature_2" %in% processed_task$feature_names)
  stopifnot(!"Condition_3" %in% processed_task$feature_names)
  stopifnot(!"Lot_Area_m2" %in% processed_task$feature_names)
  stopifnot(!any(processed_task$missings() > 0))
  
  log_step("PREPROC", "Pipeline verification passed all assertions successfully!")
}
