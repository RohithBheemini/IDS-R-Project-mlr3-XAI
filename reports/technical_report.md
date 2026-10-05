# Explainable House Price Prediction Using R and mlr3
## Technical Report & Methodological Analysis

**Author:** Antigravity Data Science Team  
**Dataset:** `mlr3data::ames_housing` (2,930 observations, 81 predictors, Target: `Sale_Price`)  
**Framework:** `mlr3` (v1.8.0), `mlr3pipelines` (v0.12.0), `mlr3tuning` (v1.7.0), `iml` (v0.11.4), `lime` (v0.5.4), `shiny` (v1.14.0)

---

### 1. Introduction & Research Objectives

The valuation of residential real estate is driven by a complex interplay of spatial, structural, chronological, and qualitative features. In machine learning, practitioners frequently prioritize predictive accuracy at the expense of explainability, deploying black-box algorithms whose decision boundaries remain opaque.

This project implements an end-to-end, reproducible, leakage-free machine learning workflow grounded in the seminal papers of the `mlr` ecosystem:
- **Paper A (Bischl et al., 2016):** Demonstrates the power of unified object-oriented machine learning architectures.
- **Paper B (Lang et al., 2019):** Modernizes ML in R with modular R6 and `data.table` design.
- **Paper C (Binder et al., 2021):** Establishes composable DAG pipelines (`mlr3pipelines`) guaranteeing that all data transformations learn parameters strictly within the training fold.
- **Applied Machine Learning Using mlr3 in R (Bischl et al., 2024):** Details the intentional educational challenges introduced into the Ames dataset.

---

### 2. Data Quality Audit & Handling of Artificial Defects

The raw dataset was subjected to a systematic data audit (`R/02_data_audit.R`). As detailed in Chapter 9 of the `mlr3` book, several artificial defects were intentionally introduced into this pedagogical dataset:
1. **Constant Feature (`Misc_Feature_2`):** Contains only 1 unique level (`Othr`). Handled via `PipeOpRemoveConstants`.
2. **Identical Duplicate (`Condition_3`):** 100% duplicate of `Condition_2`. Handled via `PipeOpSelect`.
3. **Collinear Metric Representation (`Lot_Area_m2`):** Perfectly correlated ($r = 1.000$) duplicate of `Lot_Area`. Handled via `PipeOpSelect`.
4. **Structural Missingness:** Over 90% missing values in `Pool_QC`, `Misc_Feature`, and `Alley` reflect the absence of the amenity rather than measurement attrition. Categorical factors are encoded with an explicit `MISSING` category (`PipeOpImputeOOR`), while numerical predictors are imputed with median values (`PipeOpImputeMedian`).
5. **High-Cardinality Factors:** Categories with rare levels are grouped using `PipeOpCollapseFactors` (target count 15), and unseen levels at predict time are safeguarded using post-encode zero imputation.

---

### 3. Feature Engineering

Six domain-justified features were created (`R/05_feature_engineering.R`) and empirically validated against `Sale_Price`:
- `Total_Living_Area`: Aggregates above-ground area and finished basement space ($r = 0.7315$).
- `Total_Bathrooms`: Combines full and half baths additively ($r = 0.6362$).
- `Total_Porch_SF`: Unifies disparate deck and porch variables ($r = 0.3835$).
- `Age_At_Sale`: Transaction year minus construction year ($r = -0.5589$).
- `Years_Since_Remodel`: Transaction year minus renovation year ($r = -0.5350$).
- `Qual_x_LivingArea`: Multiplicative interaction between overall quality and living area ($r = 0.8454$).

---

### 4. Cross-Validated Model Benchmarking

Six distinct model families were benchmarked across identical 5-fold cross-validation splits on 2,344 training properties:

| Model Architecture | Cross-Validation MAE (USD) | RMSE (USD) | $R^2$ Variance Explained |
| :--- | :---: | :---: | :---: |
| **Gradient Boosted Trees (XGBoost)** | **$15,321** | **$25,941** | **0.8927** |
| **Random Forest (Ranger)** | **$15,858** | **$26,183** | **0.8912** |
| **ElasticNet (Glmnet)** | **$16,749** | **$39,843** | **0.7181** |
| **Linear Regression (LM)** | **$21,093** | **$35,967** | **0.7855** |
| **Decision Tree (Rpart)** | **$27,458** | **$40,384** | **0.7432** |
| **Featureless Baseline** | **$58,761** | **$79,962** | **-0.0051** |

### Key Findings
1. Non-linear ensemble methods (`xgboost` and `ranger`) achieve superior predictive accuracy, explaining ~89.2% of the variance in sale price.
2. The regularized linear model (`glmnet`) improves over standard ordinary least squares by over $4,300 in MAE by penalizing redundant features.
3. Decision trees in isolation lack the capacity to model continuous multi-attribute valuation curves without severe variance.

---

### 5. Explainable AI & Governance

The explainability layer utilizes **SHAP** (Shapley Additive Explanations) and **LIME** (Local Interpretable Model-agnostic Explanations):
- **Global Permutation Importance:** Highlights `Qual_x_LivingArea`, `Total_Living_Area`, `Gr_Liv_Area`, `Overall_Qual`, and `Age_At_Sale` as the top 5 global drivers.
- **Local Explanations:** For individual homes, SHAP provides an additive decomposition showing how much each attribute shifted the valuation above or below the Ames market average ($180,800).
- **Non-Causal Boundary (PRD Section 12.4):** SHAP and LIME values represent **statistical model attribution** within the fitted machine learning algorithm. They do not constitute empirical causal claims, structural engineering guarantees, or professional appraisals.

---

### 6. Interactive Shiny Deployment

The application (`app/app.R`) packages the fitted predictive pipeline and explainability engine into a modern, accessible web interface:
- **Two-Tier Input Strategy:** Users can evaluate properties using intuitive primary controls (Basic Mode) or fine-tune all architectural parameters (Advanced Mode).
- **Transparent Assumptions:** Clearly documents all unexposed fields defaulted to dataset medians.
- **On-Demand Explainability:** Decouples instant price estimation from computational SHAP generation to ensure high UI responsiveness.
