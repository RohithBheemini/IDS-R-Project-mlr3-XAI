# ==============================================================================
# File: R/05_feature_engineering.R
# Purpose: Defensible domain-backed feature engineering and validation.
# PRD Ref: Section 9.1 (Candidate Features), Section 9.2 (Feature Selection),
#          Section 11.3 (Experiment Matrix E6), Section 21
# ==============================================================================

if (!exists("log_step")) {
  source(if (file.exists("R/10_utils.R")) "R/10_utils.R" else if (file.exists("../R/10_utils.R")) "../R/10_utils.R" else "10_utils.R")
}

suppressPackageStartupMessages({
  library(mlr3)
  library(mlr3data)
  library(data.table)
  library(ggplot2)
})

log_step("FE", "Initializing Feature Engineering Module...")

#' Augment an Ames Housing data.table or data.frame with defensible domain features
#' @param dt data.table or data.frame containing Ames Housing features
#' @return data.table with additional engineered columns
add_engineered_features <- function(dt) {
  dt <- copy(as.data.table(dt))

  # 1. Total Finished Living Area
  # Justification: Home valuation fundamentally assesses total conditioned, usable living area
  # Formula: Above-ground living area + finished basement area (Total_Bsmt_SF - Bsmt_Unf_SF)
  bsmt_finished <- pmax(0, dt$Total_Bsmt_SF - dt$Bsmt_Unf_SF, na.rm = TRUE)
  dt[, Total_Living_Area := Gr_Liv_Area + bsmt_finished]

  # 2. Total Bathrooms
  # Justification: Bathrooms are a premier valuation driver; full baths and half baths contribute additively
  # Formula: Full_Bath + 0.5 * Half_Bath + Bsmt_Full_Bath + 0.5 * Bsmt_Half_Bath
  dt[, Total_Bathrooms := Full_Bath + 0.5 * Half_Bath +
                          fcoalesce(as.numeric(Bsmt_Full_Bath), 0) + 0.5 * fcoalesce(as.numeric(Bsmt_Half_Bath), 0)]

  # 3. Total Porch & Outdoor Living Square Footage
  # Justification: Aggregates fragmented exterior deck and porch attributes into a unified metric
  # Formula: Wood_Deck_SF + Open_Porch_SF + Enclosed_Porch + Three_season_porch + Screen_Porch
  dt[, Total_Porch_SF := Wood_Deck_SF + Open_Porch_SF + Enclosed_Porch +
                         Three_season_porch + Screen_Porch]

  # 4. Property Age at Transaction
  # Justification: Real-estate depreciation depends heavily on chronological age at transaction date
  # Formula: max(0, Year_Sold - Year_Built)
  dt[, Age_At_Sale := pmax(0, Year_Sold - Year_Built)]

  # 5. Remodel Age / Recency
  # Justification: Properties remodeled recently command an appraisal premium over non-updated older homes
  # Formula: max(0, Year_Sold - Year_Remod_Add)
  dt[, Years_Since_Remodel := pmax(0, Year_Sold - Year_Remod_Add)]

  # 6. Quality x Size Interaction
  # Justification: An additional square foot in a high-grade luxury home has far greater marginal dollar value
  # Formula: Overall_Qual_score * Gr_Liv_Area
  # Note: Overall_Qual in mlr3data has qualitative character levels
  qual_map <- c(
    "Very_Poor" = 1, "Poor" = 2, "Fair" = 3, "Below_Average" = 4,
    "Average" = 5, "Above_Average" = 6, "Good" = 7, "Very_Good" = 8,
    "Excellent" = 9, "Very_Excellent" = 10
  )
  qual_char <- as.character(dt$Overall_Qual)
  qual_num <- qual_map[qual_char]
  qual_num[is.na(qual_num)] <- 5 # default to Average if missing
  dt[, Qual_x_LivingArea := qual_num * Gr_Liv_Area]

  return(dt)
}

#' Create an augmented mlr3 regression task containing engineered features
#' @return mlr3::TaskRegr object
create_engineered_task <- function() {
  task_raw <- tsk("ames_housing")
  dt_raw <- as.data.table(task_raw$data())
  dt_fe <- add_engineered_features(dt_raw)
  
  task_fe <- as_task_regr(dt_fe, target = "Sale_Price", id = "ames_engineered")
  return(task_fe)
}

# ------------------------------------------------------------------------------
# Feature Validation & Correlation Analysis
# ------------------------------------------------------------------------------
if (sys.nframe() == 0) {
  log_step("FE", "Evaluating correlations of engineered features with Sale_Price...")

  task_fe <- create_engineered_task()
  dt_fe <- as.data.table(task_fe$data())
  
  eng_features <- c(
    "Total_Living_Area",
    "Total_Bathrooms",
    "Total_Porch_SF",
    "Age_At_Sale",
    "Years_Since_Remodel",
    "Qual_x_LivingArea"
  )
  
  fe_correlations <- sapply(eng_features, function(f) {
    cor(dt_fe[[f]], dt_fe$Sale_Price, use = "complete.obs")
  })
  
  fe_summary <- data.frame(
    Feature = eng_features,
    Correlation_With_SalePrice = round(fe_correlations, 4),
    Expected_Direction = c("Positive", "Positive", "Positive", "Negative", "Negative", "Positive"),
    Observed_Sign = ifelse(fe_correlations > 0, "Positive", "Negative")
  )
  
  cat("\n======================================================\n")
  cat("ENGINEERED FEATURES VALIDATION SUMMARY\n")
  cat("======================================================\n")
  print(fe_summary)
  cat("======================================================\n\n")
  
  # Ensure all signs match domain expectations
  stopifnot(all(fe_summary$Expected_Direction == fe_summary$Observed_Sign))
  
  # Plot Feature Validation
  p_fe <- ggplot(fe_summary, aes(x = reorder(Feature, abs(Correlation_With_SalePrice)),
                                 y = Correlation_With_SalePrice,
                                 fill = Observed_Sign)) +
    geom_col(width = 0.6) +
    scale_fill_manual(values = c("Negative" = "#EF4444", "Positive" = "#10B981")) +
    coord_flip() +
    labs(
      title = "Correlations of Engineered Features with Sale Price",
      subtitle = "All 6 features exhibit strong alignment with real-estate domain expectations",
      x = "Engineered Feature",
      y = "Correlation (r)",
      fill = "Relationship"
    ) +
    get_project_theme()
  
  save_project_artifact(p_fe, "eda_07_engineered_features_correlations.png", dir = "figures")
  save_project_artifact(fe_summary, "engineered_features_summary.rds", dir = "reports")
  
  log_step("FE", "Feature engineering completed and verified successfully!")
}
