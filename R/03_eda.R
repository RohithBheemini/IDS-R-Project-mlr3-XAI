# ==============================================================================
# File: R/03_eda.R
# Purpose: Exploratory Data Analysis (EDA) generating diagnostic charts,
#          target distribution analysis, and correlation profiling.
# PRD Ref: Section 8 (Data Understanding), Section 20.1 (figures/ deliverables)
# ==============================================================================

source("R/10_utils.R")

suppressPackageStartupMessages({
  library(mlr3)
  library(mlr3data)
  library(data.table)
  library(ggplot2)
})

log_step("EDA", "Beginning Exploratory Data Analysis & Diagnostic Visualizations...")

if (!dir.exists("figures")) {
  dir.create("figures", recursive = TRUE)
}

task <- tsk("ames_housing")
dt <- as.data.table(task$data())

# ------------------------------------------------------------------------------
# 1. Target Distribution Plot: Sale_Price (Raw vs Log-Transformed)
# ------------------------------------------------------------------------------
log_step("EDA", "Generating Target Distribution Plots (Sale_Price)...")

p_target_raw <- ggplot(dt, aes(x = Sale_Price)) +
  geom_histogram(bins = 40, fill = "#2563EB", color = "white", alpha = 0.85) +
  geom_vline(aes(xintercept = median(Sale_Price)), color = "#DC2626", linetype = "dashed", linewidth = 1) +
  scale_x_continuous(labels = scales::dollar_format()) +
  labs(
    title = "Distribution of Ames Housing Sale Price (Raw)",
    subtitle = sprintf("Right-skewed | Median: %s | Mean: %s",
                       format_currency(median(dt$Sale_Price)),
                       format_currency(mean(dt$Sale_Price))),
    x = "Sale Price (USD)",
    y = "Frequency"
  ) +
  get_project_theme()

p_target_log <- ggplot(dt, aes(x = log10(Sale_Price))) +
  geom_histogram(bins = 40, fill = "#059669", color = "white", alpha = 0.85) +
  geom_vline(aes(xintercept = median(log10(Sale_Price))), color = "#DC2626", linetype = "dashed", linewidth = 1) +
  labs(
    title = "Distribution of Ames Housing Sale Price (Log10 Transformed)",
    subtitle = "Log transformation significantly restores bell-shaped normality",
    x = "log10(Sale Price)",
    y = "Frequency"
  ) +
  get_project_theme()

save_project_artifact(p_target_raw, "eda_01_target_distribution_raw.png", dir = "figures")
save_project_artifact(p_target_log, "eda_02_target_distribution_log.png", dir = "figures")

# ------------------------------------------------------------------------------
# 2. Top Correlated Numeric Features with Sale_Price
# ------------------------------------------------------------------------------
log_step("EDA", "Computing and plotting correlation with Sale_Price...")

numeric_cols <- names(dt)[sapply(dt, is.numeric)]
numeric_cols <- setdiff(numeric_cols, c("Sale_Price", "Lot_Area_m2")) # exclude duplicate scale

cor_vals <- sapply(numeric_cols, function(col) {
  idx <- complete.cases(dt[[col]], dt$Sale_Price)
  cor(dt[[col]][idx], dt$Sale_Price[idx])
})

cor_df <- data.frame(
  Feature = names(cor_vals),
  Correlation = as.numeric(cor_vals)
)
cor_df <- cor_df[order(-cor_df$Correlation), ]
top_pos_cor <- head(cor_df, 12)

p_cor <- ggplot(top_pos_cor, aes(x = reorder(Feature, Correlation), y = Correlation)) +
  geom_col(fill = "#3B82F6", alpha = 0.9, width = 0.7) +
  coord_flip() +
  scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, 0.2)) +
  labs(
    title = "Top 12 Numerical Predictors Correlated with Sale Price",
    subtitle = "Living Area, Quality metrics, and Garage capacity dominate Pearson correlations",
    x = "Predictor Feature",
    y = "Pearson Correlation Coefficient (r)"
  ) +
  get_project_theme()

save_project_artifact(p_cor, "eda_03_top_correlations.png", dir = "figures")

# ------------------------------------------------------------------------------
# 3. Overall Quality vs Sale Price Boxplot
# ------------------------------------------------------------------------------
log_step("EDA", "Plotting Overall_Qual relationship with Sale Price...")

p_qual <- ggplot(dt[!is.na(Overall_Qual)], aes(x = factor(Overall_Qual), y = Sale_Price)) +
  geom_boxplot(fill = "#8B5CF6", color = "#4C1D95", alpha = 0.75, outlier.size = 1) +
  scale_y_continuous(labels = scales::dollar_format()) +
  labs(
    title = "Sale Price Distribution across Overall Quality Ratings",
    subtitle = "Exponential upward trend as quality rating advances from Poor to Very Excellent",
    x = "Overall Quality Rating (1 to 10)",
    y = "Sale Price (USD)"
  ) +
  get_project_theme()

save_project_artifact(p_qual, "eda_04_overall_qual_vs_price.png", dir = "figures")

# ------------------------------------------------------------------------------
# 4. Living Area (Gr_Liv_Area) vs Sale Price Scatter with Linear Trend
# ------------------------------------------------------------------------------
log_step("EDA", "Plotting Ground Living Area vs Sale Price...")

p_scatter <- ggplot(dt, aes(x = Gr_Liv_Area, y = Sale_Price)) +
  geom_point(alpha = 0.35, color = "#2563EB", size = 1.8) +
  geom_smooth(method = "loess", color = "#EF4444", se = FALSE, linewidth = 1.1) +
  scale_y_continuous(labels = scales::dollar_format()) +
  scale_x_continuous(labels = scales::comma_format()) +
  labs(
    title = "Sale Price vs Above Ground Living Area (Gr_Liv_Area)",
    subtitle = "Strong linear trajectory with slight high-end variance",
    x = "Above Ground Living Area (sq ft)",
    y = "Sale Price (USD)"
  ) +
  get_project_theme()

save_project_artifact(p_scatter, "eda_05_gr_liv_area_vs_price.png", dir = "figures")

# ------------------------------------------------------------------------------
# 5. Missingness Profile Plot
# ------------------------------------------------------------------------------
log_step("EDA", "Plotting Missing Data Profile...")

na_counts <- sapply(dt, function(x) sum(is.na(x)))
na_df <- data.frame(
  Feature = names(na_counts),
  MissingPct = (na_counts / nrow(dt)) * 100
)
na_df <- na_df[na_df$MissingPct > 0, ]
na_df <- head(na_df[order(-na_df$MissingPct), ], 15)

p_missing <- ggplot(na_df, aes(x = reorder(Feature, MissingPct), y = MissingPct)) +
  geom_col(fill = "#F59E0B", width = 0.7) +
  coord_flip() +
  labs(
    title = "Top 15 Features by Missing Percentage",
    subtitle = "High missingness in Pool_QC, Misc_Feature, Alley represents feature absence, not data corruption",
    x = "Feature",
    y = "Missing Percentage (%)"
  ) +
  get_project_theme()

save_project_artifact(p_missing, "eda_06_missingness_profile.png", dir = "figures")

log_step("EDA", "Exploratory Data Analysis complete. All figures generated in figures/")
