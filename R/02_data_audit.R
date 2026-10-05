# ==============================================================================
# File: R/02_data_audit.R
# Purpose: Comprehensive data quality audit identifying anomalies, constants,
#          duplicates, redundant scales, missingness, and distribution issues.
# PRD Ref: Section 4.2 (Main Documented Cases), Section 8.1 (Audit Checklist),
#          Section 21 (Acceptance Criteria 2)
# ==============================================================================

source("R/10_utils.R")

suppressPackageStartupMessages({
  library(mlr3)
  library(mlr3data)
  library(data.table)
})

log_step("AUDIT", "Beginning Comprehensive Data Quality Audit...")

# Load raw task and extract data frame
task <- tsk("ames_housing")
dt <- as.data.table(task$data())

audit_report <- list()

# ------------------------------------------------------------------------------
# 1. Dimensions and Overview
# ------------------------------------------------------------------------------
log_step("AUDIT", "1. Assessing dataset dimensions and variable types...")
n_rows <- nrow(dt)
n_cols <- ncol(dt)
feature_names <- setdiff(names(dt), "Sale_Price")

type_counts <- table(sapply(dt[, ..feature_names], function(x) class(x)[1]))
cat(sprintf("Total Observations : %d\n", n_rows))
cat(sprintf("Total Columns      : %d (1 target + %d predictors)\n", n_cols, length(feature_names)))
cat("Feature types:\n")
print(type_counts)

# ------------------------------------------------------------------------------
# 2. Constant & Near-Constant Features
# PRD Ref: Misc_Feature_2 has only one level
# ------------------------------------------------------------------------------
log_step("AUDIT", "2. Auditing Constant & Near-Constant features...")
unique_counts <- sapply(dt[, ..feature_names], function(col) uniqueN(col, na.rm = TRUE))
constant_features <- names(unique_counts[unique_counts <= 1])

cat(sprintf("Found %d strictly constant feature(s):\n", length(constant_features)))
for (cf in constant_features) {
  val <- unique(dt[[cf]][!is.na(dt[[cf]])])
  cat(sprintf("  - '%s': single level '%s' (NAs: %d)\n", cf, as.character(val), sum(is.na(dt[[cf]]))))
}

# ------------------------------------------------------------------------------
# 3. Duplicate Feature Check
# PRD Ref: Condition_2 and Condition_3 are identical
# ------------------------------------------------------------------------------
log_step("AUDIT", "3. Auditing Duplicate/Identical features...")
duplicate_pairs <- list()
for (i in 1:(length(feature_names) - 1)) {
  for (j in (i + 1):length(feature_names)) {
    f1 <- feature_names[i]
    f2 <- feature_names[j]
    if (identical(dt[[f1]], dt[[f2]])) {
      duplicate_pairs[[length(duplicate_pairs) + 1]] <- c(f1, f2)
      cat(sprintf("  - IDENTICAL DUPLICATE FOUND: '%s' and '%s'\n", f1, f2))
    }
  }
}

# ------------------------------------------------------------------------------
# 4. Same Information on Different Scales / Collinearity
# PRD Ref: Lot_Area and Lot_Area_m2 are perfectly correlated
# ------------------------------------------------------------------------------
log_step("AUDIT", "4. Auditing Redundant Scaled Representations & Collinearity...")
numeric_features <- names(dt[, ..feature_names])[sapply(dt[, ..feature_names], is.numeric)]

collinear_pairs <- list()
for (i in 1:(length(numeric_features) - 1)) {
  for (j in (i + 1):length(numeric_features)) {
    nf1 <- numeric_features[i]
    nf2 <- numeric_features[j]
    complete_idx <- complete.cases(dt[[nf1]], dt[[nf2]])
    if (sum(complete_idx) > 100) {
      r <- suppressWarnings(cor(dt[[nf1]][complete_idx], dt[[nf2]][complete_idx]))
      if (!is.na(r) && abs(r) > 0.9999) {
        collinear_pairs[[length(collinear_pairs) + 1]] <- c(nf1, nf2, round(r, 6))
        cat(sprintf("  - PERFECT REDUNDANT SCALE: '%s' & '%s' (r = %.6f)\n", nf1, nf2, r))
      }
    }
  }
}

# ------------------------------------------------------------------------------
# 5. Missingness Profile
# ------------------------------------------------------------------------------
log_step("AUDIT", "5. Auditing Missing Data Profile...")
na_counts <- sapply(dt, function(x) sum(is.na(x)))
na_pct    <- round((na_counts / n_rows) * 100, 2)
missing_df <- data.frame(
  Feature = names(na_counts),
  Missing_Count = na_counts,
  Missing_Percent = na_pct
)[na_counts > 0, ]
missing_df <- missing_df[order(-missing_df$Missing_Count), ]

cat(sprintf("Found %d features with missing values. Top missing features:\n", nrow(missing_df)))
print(head(missing_df, 10))

# ------------------------------------------------------------------------------
# 6. Target Distribution & Skewness (Sale_Price)
# ------------------------------------------------------------------------------
log_step("AUDIT", "6. Auditing Target Distribution (Sale_Price)...")
sp <- dt$Sale_Price
sp_summary <- summary(sp)
sp_iqr <- IQR(sp)
sp_skew <- (mean(sp) - median(sp)) / sd(sp) # Pearson skew coefficient approx

cat("Sale_Price Summary Statistics (USD):\n")
print(sp_summary)
cat(sprintf("Standard Deviation: $%.2f\n", sd(sp)))
cat(sprintf("Skewness Metric   : %.4f (Right-skewed tail indicated)\n", sp_skew))

# ------------------------------------------------------------------------------
# 7. Semantic & Range Checks
# ------------------------------------------------------------------------------
log_step("AUDIT", "7. Auditing Range & Logical Consistency...")
semantic_issues <- list()

# Check negative areas
area_cols <- grep("Area|SF|Square", names(dt), value = TRUE)
for (ac in area_cols) {
  if (is.numeric(dt[[ac]])) {
    neg_count <- sum(dt[[ac]] < 0, na.rm = TRUE)
    if (neg_count > 0) {
      cat(sprintf("  - Warning: Feature '%s' has %d negative values!\n", ac, neg_count))
      semantic_issues[[ac]] <- paste0(neg_count, " negative values")
    }
  }
}

# Check Year_Remod_Add vs Year_Built
if ("Year_Remod_Add" %in% names(dt) && "Year_Built" %in% names(dt)) {
  invalid_remod <- sum(dt$Year_Remod_Add < dt$Year_Built, na.rm = TRUE)
  cat(sprintf("  - Year_Remod_Add < Year_Built occurrences: %d\n", invalid_remod))
}

# Compile and persist full audit findings
audit_report <- list(
  total_rows = n_rows,
  total_features = length(feature_names),
  constant_features = constant_features,
  duplicate_pairs = duplicate_pairs,
  collinear_pairs = collinear_pairs,
  missing_df = missing_df,
  target_stats = as.list(sp_summary),
  timestamp = Sys.time()
)

save_project_artifact(audit_report, "data_audit_report.rds", dir = "reports")
log_step("AUDIT", "Data quality audit complete. Saved to reports/data_audit_report.rds")
