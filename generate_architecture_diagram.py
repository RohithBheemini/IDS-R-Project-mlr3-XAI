#!/usr/bin/env python3
"""
generate_architecture_diagram.py
Generates an ultra-high-resolution, professional, publication-quality architecture diagram
for the Explainable House Price Prediction & Production System.
Outputs:
  - architecture.png (Lossless high-res PNG)
  - architecture.jpg (High-quality JPEG)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

# -----------------------------------------------------------------------------
# Canvas Setup
# -----------------------------------------------------------------------------
FIG_WIDTH = 24.0   # inches
FIG_HEIGHT = 15.0  # inches
DPI = 300          # High-resolution print quality (7200 x 4500 px)

fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=DPI)
ax.set_xlim(0, 24)
ax.set_ylim(0, 15)
ax.axis('off')

# Background: Deep executive dark slate canvas
fig.patch.set_facecolor('#0B0F19')
ax.set_facecolor('#0B0F19')

# -----------------------------------------------------------------------------
# Color Palette (Modern Executive Cloud Architecture)
# -----------------------------------------------------------------------------
COLOR_BG_CARD    = '#131B2E'   # Card background
COLOR_BORDER     = '#1E293B'   # Card border
COLOR_HEADER_BG  = '#1E293B'   # Sub-header background
COLOR_TEXT_WHITE = '#F8FAFC'   # Primary text
COLOR_TEXT_MUTED = '#94A3B8'   # Secondary muted text
COLOR_TEXT_DIM   = '#64748B'   # Tertiary dim text

# Accent Colors for System Tiers
COLOR_CYAN       = '#06B6D4'   # Ingestion & Data Quality
COLOR_BLUE       = '#3B82F6'   # Leakage-Safe DAG Pipeline
COLOR_PURPLE     = '#8B5CF6'   # Model Tournament & Tuning
COLOR_GREEN      = '#10B981'   # Evaluation & Dual XAI
COLOR_ORANGE     = '#F59E0B'   # Production Serving & Cloud Scale

# -----------------------------------------------------------------------------
# Helper Drawing Functions
# -----------------------------------------------------------------------------
def draw_card(ax, x, y, w, h, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER, corner_radius=0.15, alpha=0.95):
    """Draws a rounded card container with crisp borders."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={corner_radius}",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=1.5,
        alpha=alpha,
        zorder=2
    )
    ax.add_patch(box)
    return box

def draw_badge(ax, x, y, text, color=COLOR_BLUE, text_color='#FFFFFF', fontsize=9):
    """Draws a pill badge label."""
    w = len(text) * 0.088 + 0.35
    h = 0.32
    badge = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.1",
        facecolor=color,
        edgecolor='none',
        zorder=5
    )
    ax.add_patch(badge)
    ax.text(x + w/2, y + h/2, text, color=text_color, fontsize=fontsize,
            fontweight='bold', ha='center', va='center', zorder=6, fontfamily='sans-serif')
    return w

def draw_arrow(ax, x1, y1, x2, y2, color='#38BDF8', width=2.0, style='->', label=None):
    """Draws a clean directional flow arrow with optional label."""
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle=style,
            color=color,
            lw=width,
            shrinkA=4,
            shrinkB=4,
            mutation_scale=15
        ),
        zorder=10
    )
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.12, label, color=color, fontsize=8.5,
                fontweight='bold', ha='center', va='center', zorder=11,
                bbox=dict(boxstyle="round,pad=0.15", facecolor='#0B0F19', edgecolor='none', alpha=0.9))

# -----------------------------------------------------------------------------
# 1. HEADER SECTION (Top Title & Subtitle)
# -----------------------------------------------------------------------------
# Top accent decorative line
ax.plot([0.8, 23.2], [14.45, 14.45], color=COLOR_BLUE, lw=2.5, zorder=3)

ax.text(0.8, 14.1, "ENTERPRISE EXPLAINABLE AI (XAI) HOUSING VALUATION PLATFORM",
        color=COLOR_TEXT_WHITE, fontsize=21, fontweight='black', fontfamily='sans-serif', zorder=5)

ax.text(0.8, 13.72, "End-to-End Production Architecture  •  Zero-Leakage mlr3 DAG  •  Dual XAI Engine (SHAP & LIME)  •  Cloud Microservices & Serving",
        color=COLOR_CYAN, fontsize=11.5, fontweight='bold', fontfamily='sans-serif', zorder=5)

# Version & Compliance Badges in Header Right
draw_badge(ax, 18.2, 13.9, "R v4.6.1 + mlr3 ecosystem", color='#1E293B', text_color='#38BDF8', fontsize=9.5)
draw_badge(ax, 20.8, 13.9, "Production Blueprint v2.0", color='#059669', text_color='#FFFFFF', fontsize=9.5)

# -----------------------------------------------------------------------------
# 2. COLUMN / TIER ARCHITECTURE LAYOUT (5 Horizontal Flow Tiers)
# -----------------------------------------------------------------------------
# Layout bounds:
# Column 1: Ingestion & Forensics   [x: 0.8  -> 4.9]
# Column 2: Leakage-Safe DAG         [x: 5.3  -> 9.4]
# Column 3: Model Tournament & Tune  [x: 9.8  -> 13.9]
# Column 4: Holdout & Dual XAI       [x: 14.3 -> 18.4]
# Column 5: Production Serving & API [x: 18.8 -> 23.2]

Y_TIER_TOP    = 13.3
Y_TIER_HEIGHT = 10.4

# =============================================================================
# TIER 1: INGESTION & DATA FORENSICS (Cyan Accent)
# =============================================================================
col1_x = 0.8
col1_w = 4.2
draw_card(ax, col1_x, Y_TIER_TOP - Y_TIER_HEIGHT, col1_w, Y_TIER_HEIGHT,
          bg_color='#0E1726', border_color=COLOR_CYAN)

# Header banner for Tier 1
patches_t1 = patches.FancyBboxPatch((col1_x, Y_TIER_TOP - 0.75), col1_w, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.15",
                                    facecolor='#16253B', edgecolor=COLOR_CYAN, linewidth=1.5, zorder=3)
ax.add_patch(patches_t1)
ax.text(col1_x + col1_w/2, Y_TIER_TOP - 0.38, "1. INGESTION & FORENSICS",
        color='#38BDF8', fontsize=12, fontweight='bold', ha='center', va='center', zorder=4)

# Box 1.1: Raw Ames Ingestion
draw_card(ax, col1_x + 0.2, 10.5, col1_w - 0.4, 1.8, bg_color='#131F33', border_color='#253A5A')
ax.text(col1_x + 0.35, 12.0, "Canonical Ames Housing Data", color=COLOR_TEXT_WHITE, fontsize=10.5, fontweight='bold')
ax.text(col1_x + 0.35, 11.75, "Source: mlr3data::ames_housing", color='#38BDF8', fontsize=9)
t1_lines = [
    "• Total Properties: 2,930 Transactions (Ames, IA)",
    "• Raw Features: 81 (47 factors, 33 int, 1 numeric)",
    "• Target: Sale_Price ($34.9k to $755k; mean $180.8k)"
]
for idx, line in enumerate(t1_lines):
    ax.text(col1_x + 0.35, 11.4 - idx*0.3, line, color=COLOR_TEXT_MUTED, fontsize=8.8)

# Box 1.2: Forensic Data Quality Audit
draw_card(ax, col1_x + 0.2, 7.8, col1_w - 0.4, 2.45, bg_color='#131F33', border_color='#EF4444')
draw_badge(ax, col1_x + 0.35, 9.9, "DEFECT AUDIT (PRD §4.2)", color='#991B1B', text_color='#FECACA', fontsize=8)
t1_audit = [
    ("Trap 1: Constant Feature (Misc_Feature_2)", "• Zero variance across all 2,930 rows -> DROPPED", '#F87171'),
    ("Trap 2: Exact Duplicate (Condition_3)", "• 100% cloned copy of Condition_2 -> PRUNED", '#F87171'),
    ("Trap 3: Collinear Scale (Lot_Area_m2)", "• Exact conversion: Lot_Area * 0.0929 -> PRUNED", '#F87171'),
    ("Semantic Missingness Audit", "• NA = 'No Garage/Pool/Fireplace' (not error!)", '#38BDF8')
]
y_cursor = 9.55
for title, desc, clr in t1_audit:
    ax.text(col1_x + 0.35, y_cursor, title, color=COLOR_TEXT_WHITE, fontsize=8.8, fontweight='bold')
    ax.text(col1_x + 0.35, y_cursor - 0.22, desc, color=clr, fontsize=8.2)
    y_cursor -= 0.52

# Box 1.3: Stratified Partitioning
draw_card(ax, col1_x + 0.2, 3.2, col1_w - 0.4, 4.35, bg_color='#131F33', border_color='#253A5A')
ax.text(col1_x + 0.35, 7.25, "Data Partitioning (Strict Separation)", color=COLOR_TEXT_WHITE, fontsize=10.5, fontweight='bold')

# Sub-partition A: 80% Train
draw_card(ax, col1_x + 0.35, 5.25, col1_w - 0.7, 1.75, bg_color='#1A2E4C', border_color='#0284C7')
ax.text(col1_x + 0.5, 6.7, "80% Training Resampling Pool", color='#38BDF8', fontsize=10, fontweight='bold')
ax.text(col1_x + 0.5, 6.4, "• 2,344 Properties", color=COLOR_TEXT_WHITE, fontsize=9, fontweight='bold')
ax.text(col1_x + 0.5, 6.1, "• Strictly for 5-Fold Cross Validation", color=COLOR_TEXT_MUTED, fontsize=8.5)
ax.text(col1_x + 0.5, 5.8, "• Learns all imputation & encodings", color=COLOR_TEXT_MUTED, fontsize=8.5)
ax.text(col1_x + 0.5, 5.5, "• Output: reports/dataset_partitions.rds", color='#06B6D4', fontsize=8)

# Sub-partition B: 20% Holdout
draw_card(ax, col1_x + 0.35, 3.4, col1_w - 0.7, 1.65, bg_color='#1E293B', border_color='#EF4444')
ax.text(col1_x + 0.5, 4.75, "20% Locked Holdout Test Set", color='#F87171', fontsize=10, fontweight='bold')
ax.text(col1_x + 0.5, 4.45, "• 586 Completely Untouched Properties", color=COLOR_TEXT_WHITE, fontsize=9, fontweight='bold')
ax.text(col1_x + 0.5, 4.15, "• Locked until final model certification", color=COLOR_TEXT_MUTED, fontsize=8.5)
ax.text(col1_x + 0.5, 3.85, "• Zero data leakage / zero snooping", color='#FCA5A5', fontsize=8.5)
ax.text(col1_x + 0.5, 3.55, "• Gold-standard generalization test", color=COLOR_TEXT_MUTED, fontsize=8)

# =============================================================================
# TIER 2: LEAKAGE-SAFE DAG PREPROCESSING (Blue Accent)
# =============================================================================
col2_x = 5.3
col2_w = 4.2
draw_card(ax, col2_x, Y_TIER_TOP - Y_TIER_HEIGHT, col2_w, Y_TIER_HEIGHT,
          bg_color='#0B192E', border_color=COLOR_BLUE)

patches_t2 = patches.FancyBboxPatch((col2_x, Y_TIER_TOP - 0.75), col2_w, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.15",
                                    facecolor='#172B4D', edgecolor=COLOR_BLUE, linewidth=1.5, zorder=3)
ax.add_patch(patches_t2)
ax.text(col2_x + col2_w/2, Y_TIER_TOP - 0.38, "2. LEAKAGE-SAFE DAG PIPELINE",
        color='#60A5FA', fontsize=12, fontweight='bold', ha='center', va='center', zorder=4)

# Box 2.1: mlr3pipelines DAG Engine
draw_card(ax, col2_x + 0.2, 8.4, col2_w - 0.4, 3.9, bg_color='#10223D', border_color='#1D4ED8')
ax.text(col2_x + 0.35, 12.0, "DAG Preprocessing Graph (PipeOps)", color=COLOR_TEXT_WHITE, fontsize=10.5, fontweight='bold')
ax.text(col2_x + 0.35, 11.72, "mlr3pipelines execution graph: Zero Leakage", color='#60A5FA', fontsize=8.5)

dag_nodes = [
    ("1. PipeOpRemoveConstants", "Auto-purges zero-variance columns"),
    ("2. PipeOpSelect", "Explicitly prunes Condition_3 & Lot_Area_m2"),
    ("3. PipeOpImputeMedian", "Continuous metrics get fold-median values"),
    ("4. PipeOpImputeOOR", "Categoricals get explicit 'MISSING' level"),
    ("5. PipeOpCollapseFactors", "Rare levels collapsed (threshold 15 bins)"),
    ("6. PipeOpEncode", "One-hot treatment dummy encoding"),
    ("7. PipeOpImputeConstant(0)", "Post-encode zero-fills unseen test levels")
]
y_dag = 11.35
for n_title, n_sub in dag_nodes:
    draw_card(ax, col2_x + 0.35, y_dag - 0.38, col2_w - 0.7, 0.45, bg_color='#162E52', border_color='#2563EB', corner_radius=0.08)
    ax.text(col2_x + 0.5, y_dag - 0.13, n_title, color='#93C5FD', fontsize=8.5, fontweight='bold')
    ax.text(col2_x + 0.5, y_dag - 0.30, n_sub, color=COLOR_TEXT_MUTED, fontsize=7.8)
    y_dag -= 0.52

# Box 2.2: Domain Feature Engineering Module
draw_card(ax, col2_x + 0.2, 3.2, col2_w - 0.4, 4.95, bg_color='#10223D', border_color='#059669')
draw_badge(ax, col2_x + 0.35, 7.85, "DOMAIN FEATURE SCIENCE (R/05_feature_engineering.R)", color='#065F46', text_color='#A7F3D0', fontsize=8)

fe_items = [
    ("Qual_x_LivingArea  (r = 0.8454)", "• Quality Rating (1-10) x Gr_Liv_Area\n• Single strongest driver (+0.14 correlation lift)", '#10B981'),
    ("Total_Living_Area", "• Gr_Liv_Area + (Total_Bsmt_SF - Bsmt_Unf_SF)\n• Combines finished basement & above-ground", '#60A5FA'),
    ("Total_Bathrooms", "• Full_Bath + 0.5*Half_Bath + Basement Baths\n• Consolidated continuous sanitary utility", '#60A5FA'),
    ("Total_Porch_SF", "• Wood_Deck + Open_Porch + Enclosed + Screen\n• Aggregates fragmented outdoor space", '#60A5FA'),
    ("Age_At_Sale & Years_Since_Remodel", "• max(0, Year_Sold - Year_Built)\n• Separates era age from modern renovation", '#60A5FA')
]
y_fe = 7.5
for f_name, f_desc, f_clr in fe_items:
    draw_card(ax, col2_x + 0.35, y_fe - 0.65, col2_w - 0.7, 0.72, bg_color='#172C46', border_color=f_clr, corner_radius=0.08)
    ax.text(col2_x + 0.45, y_fe - 0.15, f_name, color=f_clr, fontsize=8.8, fontweight='bold')
    for sub_idx, sub_l in enumerate(f_desc.split('\n')):
        ax.text(col2_x + 0.45, y_fe - 0.35 - sub_idx*0.18, sub_l, color=COLOR_TEXT_MUTED, fontsize=7.6)
    y_fe -= 0.82

# =============================================================================
# TIER 3: MODEL TOURNAMENT & TUNING (Purple Accent)
# =============================================================================
col3_x = 9.8
col3_w = 4.2
draw_card(ax, col3_x, Y_TIER_TOP - Y_TIER_HEIGHT, col3_w, Y_TIER_HEIGHT,
          bg_color='#15112B', border_color=COLOR_PURPLE)

patches_t3 = patches.FancyBboxPatch((col3_x, Y_TIER_TOP - 0.75), col3_w, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.15",
                                    facecolor='#261C4E', edgecolor=COLOR_PURPLE, linewidth=1.5, zorder=3)
ax.add_patch(patches_t3)
ax.text(col3_x + col3_w/2, Y_TIER_TOP - 0.38, "3. BENCHMARKING & TUNING",
        color='#C084FC', fontsize=12, fontweight='bold', ha='center', va='center', zorder=4)

# Box 3.1: 5-Fold Cross Validation Tournament
draw_card(ax, col3_x + 0.2, 7.5, col3_w - 0.4, 4.8, bg_color='#1A1536', border_color='#7C3AED')
ax.text(col3_x + 0.35, 12.0, "5-Fold CV Tournament (6 Families)", color=COLOR_TEXT_WHITE, fontsize=10.5, fontweight='bold')
ax.text(col3_x + 0.35, 11.75, "Identical 5-fold splits across 2,344 properties", color='#C084FC', fontsize=8.5)

models_perf = [
    ("1. XGBoost", "$15,321", "0.8927", "#10B981"),
    ("2. Random Forest (Ranger)", "$15,858", "0.8912", "#A855F7"),
    ("3. ElasticNet (Glmnet)", "$16,749", "0.7181", "#60A5FA"),
    ("4. Linear Regression", "$21,093", "0.7855", "#94A3B8"),
    ("5. Decision Tree (Rpart)", "$27,458", "0.7432", "#94A3B8"),
    ("6. Featureless Baseline", "$58,761", "-0.0051", "#EF4444")
]
y_m = 11.4
for m_name, m_mae, m_r2, m_c in models_perf:
    draw_card(ax, col3_x + 0.35, y_m - 0.45, col3_w - 0.7, 0.52, bg_color='#231B47', border_color=m_c, corner_radius=0.08)
    ax.text(col3_x + 0.48, y_m - 0.17, m_name, color=m_c, fontsize=8.8, fontweight='bold')
    ax.text(col3_x + 0.48, y_m - 0.35, f"CV MAE: {m_mae}  |  R²: {m_r2}", color=COLOR_TEXT_WHITE, fontsize=8.0)
    y_m -= 0.58

# Decision Highlight Card
draw_card(ax, col3_x + 0.35, 7.6, col3_w - 0.7, 0.78, bg_color='#2C1E55', border_color='#C084FC', corner_radius=0.08)
ax.text(col3_x + 0.45, 8.2, "CHAMPION DECISION: Random Forest", color='#E9D5FF', fontsize=8.8, fontweight='bold')
ax.text(col3_x + 0.45, 8.0, "• Matches XGBoost ($537 gap) with zero divergence risk", color=COLOR_TEXT_MUTED, fontsize=7.6)
ax.text(col3_x + 0.45, 7.8, "• Native tree stability for certified SHAP explainability", color=COLOR_TEXT_MUTED, fontsize=7.6)

# Box 3.2: Hyperparameter Optimization Engine
draw_card(ax, col3_x + 0.2, 3.2, col3_w - 0.4, 4.05, bg_color='#1A1536', border_color='#A855F7')
draw_badge(ax, col3_x + 0.35, 6.95, "mlr3tuning + paradox SEARCH SPACE", color='#581C87', text_color='#F3E8FF', fontsize=8)

tune_params = [
    ("ranger.mtry = 44", "[15, 70]", "Subsample features per split (allows interaction splits)"),
    ("ranger.min.node.size = 4", "[2, 15]", "Terminal leaf size (captures neighborhood nuances)"),
    ("ranger.sample.fraction = 0.8916", "[0.60, 0.95]", "Bagging subsample ratio (dampens out-of-bag jitter)"),
    ("Tuning Budget", "3-Fold Inner CV", "Random Search over continuous parameter space")
]
y_t = 6.65
for p_title, p_range, p_desc in tune_params:
    draw_card(ax, col3_x + 0.35, y_t - 0.65, col3_w - 0.7, 0.72, bg_color='#241B47', border_color='#7C3AED', corner_radius=0.08)
    ax.text(col3_x + 0.45, y_t - 0.16, p_title, color='#F3E8FF', fontsize=8.6, fontweight='bold')
    ax.text(col3_x + 0.45, y_t - 0.35, f"Search: {p_range}", color='#C084FC', fontsize=7.8)
    ax.text(col3_x + 0.45, y_t - 0.52, p_desc, color=COLOR_TEXT_MUTED, fontsize=7.4)
    y_t -= 0.82

# =============================================================================
# TIER 4: HOLDOUT EVALUATION & DUAL XAI ENGINE (Green Accent)
# =============================================================================
col4_x = 14.3
col4_w = 4.2
draw_card(ax, col4_x, Y_TIER_TOP - Y_TIER_HEIGHT, col4_w, Y_TIER_HEIGHT,
          bg_color='#0C1B1A', border_color=COLOR_GREEN)

patches_t4 = patches.FancyBboxPatch((col4_x, Y_TIER_TOP - 0.75), col4_w, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.15",
                                    facecolor='#123329', edgecolor=COLOR_GREEN, linewidth=1.5, zorder=3)
ax.add_patch(patches_t4)
ax.text(col4_x + col4_w/2, Y_TIER_TOP - 0.38, "4. EVALUATION & DUAL XAI",
        color='#34D399', fontsize=12, fontweight='bold', ha='center', va='center', zorder=4)

# Box 4.1: Locked Holdout Certification (586 Untouched Homes)
draw_card(ax, col4_x + 0.2, 8.4, col4_w - 0.4, 3.9, bg_color='#102B24', border_color='#059669')
ax.text(col4_x + 0.35, 12.0, "Holdout Test Certification (586 Homes)", color=COLOR_TEXT_WHITE, fontsize=10.5, fontweight='bold')
ax.text(col4_x + 0.35, 11.75, "Locked independent test set: PRD targets met", color='#34D399', fontsize=8.5)

# 4 KPI Tiles Grid inside Box 4.1
kpi_coords = [
    (col4_x + 0.35, 10.45, "$14,761", "MAE (Holdout)", "< $16k target", '#10B981'),
    (col4_x + 2.25, 10.45, "89.79%", "R² Generalization", "> 85.0% target", '#10B981'),
    (col4_x + 0.35, 9.15, "$25,320", "RMSE Error", "Tail-robust", '#6EE7B7'),
    (col4_x + 2.25, 9.15, "9.98%", "MAPE Percent", "< 10% average", '#6EE7B7')
]
for k_x, k_y, k_val, k_lbl, k_sub, k_clr in kpi_coords:
    draw_card(ax, k_x, k_y - 0.65, 1.75, 1.15, bg_color='#16382F', border_color=k_clr, corner_radius=0.08)
    ax.text(k_x + 0.88, k_y + 0.25, k_val, color=k_clr, fontsize=14, fontweight='bold', ha='center')
    ax.text(k_x + 0.88, k_y - 0.05, k_lbl, color=COLOR_TEXT_WHITE, fontsize=8.2, fontweight='bold', ha='center')
    ax.text(k_x + 0.88, k_y - 0.32, k_sub, color=COLOR_TEXT_MUTED, fontsize=7.4, ha='center')

ax.text(col4_x + 0.35, 8.6, "Residual Diagnostics: Symmetric bell-curve centered at $0.", color='#A7F3D0', fontsize=8.0)

# Box 4.2: Dual Explainable AI Engine
draw_card(ax, col4_x + 0.2, 3.2, col4_w - 0.4, 4.95, bg_color='#102B24', border_color='#10B981')
draw_badge(ax, col4_x + 0.35, 7.85, "DUAL XAI ENGINE (SHAP + LIME)", color='#047857', text_color='#D1FAE5', fontsize=8)

xai_components = [
    ("Global Permutation Importance (iml)", "• Evaluates out-of-sample MAE loss degradation\n• Qual_x_LivingArea & Total_Living_Area > 50% power\n• Neighborhood & Age_At_Sale follow closely", '#34D399'),
    ("Local SHAP Waterfall (Game Theory)", "• Shapley additive decomposition vs $180,800 base\n• Fair payout allocations: efficiency & symmetry\n• Luxury case ($378k): +$82k Area, +$54k Qual, -$18k Age", '#60A5FA'),
    ("LIME Local Sparse Surrogates", "• Local linear surrogate rules in data neighborhood\n• Generates sparse human-interpretable constraints", '#FBBF24'),
    ("Non-Causal Governance Boundary", "• Model attribution != structural causality (PRD §12.4)\n• Satisfies Fair Housing Act & ECOA audit compliance", '#F87171')
]
y_xai = 7.5
for x_title, x_desc, x_clr in xai_components:
    draw_card(ax, col4_x + 0.35, y_xai - 0.65, col4_w - 0.7, 0.72, bg_color='#16382F', border_color=x_clr, corner_radius=0.08)
    ax.text(col4_x + 0.45, y_xai - 0.15, x_title, color=x_clr, fontsize=8.6, fontweight='bold')
    for sub_i, sub_line in enumerate(x_desc.split('\n')):
        ax.text(col4_x + 0.45, y_xai - 0.35 - sub_i*0.18, sub_line, color=COLOR_TEXT_MUTED, fontsize=7.4)
    y_xai -= 0.82

# =============================================================================
# TIER 5: PRODUCTION SERVING & CLOUD SCALE (Orange Accent)
# =============================================================================
col5_x = 18.8
col5_w = 4.4
draw_card(ax, col5_x, Y_TIER_TOP - Y_TIER_HEIGHT, col5_w, Y_TIER_HEIGHT,
          bg_color='#1E160C', border_color=COLOR_ORANGE)

patches_t5 = patches.FancyBboxPatch((col5_x, Y_TIER_TOP - 0.75), col5_w, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.15",
                                    facecolor='#3D270E', edgecolor=COLOR_ORANGE, linewidth=1.5, zorder=3)
ax.add_patch(patches_t5)
ax.text(col5_x + col5_w/2, Y_TIER_TOP - 0.38, "5. PRODUCTION SERVING & API",
        color='#FBBF24', fontsize=12, fontweight='bold', ha='center', va='center', zorder=4)

# Box 5.1: Interactive Shiny Web Application
draw_card(ax, col5_x + 0.2, 8.8, col5_w - 0.4, 3.5, bg_color='#2A1C0E', border_color='#D97706')
ax.text(col5_x + 0.35, 12.0, "Interactive Shiny Platform (app/app.R)", color=COLOR_TEXT_WHITE, fontsize=10.5, fontweight='bold')
ax.text(col5_x + 0.35, 11.75, "bslib UI / Real-Time Valuation Engine", color='#FBBF24', fontsize=8.5)

shiny_features = [
    ("1-Click Archetype Presets", "Starter ($129k), Median ($179k), Luxury ($328k)"),
    ("What-If Sensitivity Curve", "Live trajectory across 800 to 3,600 sq ft"),
    ("Live Marginal Value Badges", "+200 sq ft (+16k), +1 Bath (+9.5k), Remodel (+12k)"),
    ("Model Transparency Audit", "Explicit medians for 60+ unexposed attributes")
]
y_sh = 11.4
for sf_t, sf_d in shiny_features:
    draw_card(ax, col5_x + 0.35, y_sh - 0.42, col5_w - 0.7, 0.50, bg_color='#382210', border_color='#B45309', corner_radius=0.08)
    ax.text(col5_x + 0.48, y_sh - 0.16, sf_t, color='#FDE68A', fontsize=8.6, fontweight='bold')
    ax.text(col5_x + 0.48, y_sh - 0.34, sf_d, color=COLOR_TEXT_MUTED, fontsize=7.6)
    y_sh -= 0.56

# Box 5.2: Production Cloud Microservices & Scalability
draw_card(ax, col5_x + 0.2, 3.2, col5_w - 0.4, 5.35, bg_color='#2A1C0E', border_color='#F59E0B')
draw_badge(ax, col5_x + 0.35, 8.25, "PRODUCTION CLOUD ARCHITECTURE", color='#78350F', text_color='#FEF3C7', fontsize=8)

cloud_tiers = [
    ("REST API Microservice (R Plumber)", "• Endpoints: POST /predict, POST /explain, GET /health\n• Returns sub-20ms valuation & SHAP attribution payloads", '#FBBF24'),
    ("Containerization (Docker & renv.lock)", "• Reproducible locked environment manifest\n• Multi-stage minimal R runtime image", '#60A5FA'),
    ("High-Availability Cloud Serving", "• Kubernetes (EKS/GKE) / AWS ECS auto-scaling\n• Load-balanced behind NGINX / Cloudflare", '#34D399'),
    ("Redis In-Memory Feature & Query Cache", "• Caches repetitive SHAP calculations (< 5ms response)\n• Session state persistence for interactive users", '#F472B6'),
    ("Observability & Drift Monitoring", "• Prometheus metrics + Grafana monitoring dashboards\n• Evidently AI tracks data drift & model decay", '#A78BFA'),
    ("Automated CI/CD Quality Gateways", "• GitHub Actions runs verify_endpoints.R & demo_test.R\n• Automatic artifact build & Git versioning", '#38BDF8')
]
y_cld = 7.9
for c_title, c_desc, c_col in cloud_tiers:
    draw_card(ax, col5_x + 0.35, y_cld - 0.52, col5_w - 0.7, 0.60, bg_color='#382210', border_color=c_col, corner_radius=0.08)
    ax.text(col5_x + 0.45, y_cld - 0.14, c_title, color=c_col, fontsize=8.4, fontweight='bold')
    for ci, cl in enumerate(c_desc.split('\n')):
        ax.text(col5_x + 0.45, y_cld - 0.32 - ci*0.16, cl, color=COLOR_TEXT_MUTED, fontsize=7.2)
    y_cld -= 0.66

# -----------------------------------------------------------------------------
# 3. INTER-TIER DATAFLOW ARROWS (Connecting the System Stages)
# -----------------------------------------------------------------------------
# Arrow 1 -> 2: From Partition to DAG
draw_arrow(ax, 5.0, 6.2, 5.3, 6.2, color='#38BDF8', width=2.5, label="2,344 Train Homes")

# Arrow 2 -> 3: From DAG to Benchmark Tournament
draw_arrow(ax, 9.5, 9.8, 9.8, 9.8, color='#818CF8', width=2.5, label="Preprocessed Matrices")

# Arrow 3 -> 4: Tuned Pipeline to Holdout Evaluation
draw_arrow(ax, 14.0, 9.8, 14.3, 9.8, color='#34D399', width=2.5, label="Champion Model")

# Arrow 4 -> 5: Evaluated Pipeline to Serving & API
draw_arrow(ax, 18.5, 9.8, 18.8, 9.8, color='#FBBF24', width=2.5, label="final_model_pipeline.rds")

# Bottom Feedback loop: 1.3 Holdout set -> 4.1 Test Evaluation
ax.annotate(
    '', xy=(14.5, 8.4), xytext=(4.8, 4.0),
    arrowprops=dict(
        arrowstyle='->',
        color='#F87171',
        lw=2.0,
        linestyle='dashed',
        connectionstyle="arc3,rad=-0.18"
    ),
    zorder=10
)
ax.text(9.5, 4.8, "Locked 586 Holdout Homes (Unseen Test Data)", color='#FCA5A5',
        fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=11,
        bbox=dict(boxstyle="round,pad=0.2", facecolor='#1E1622', edgecolor='#EF4444', alpha=0.9))

# -----------------------------------------------------------------------------
# 4. FOOTER STATUS BAR
# -----------------------------------------------------------------------------
draw_card(ax, 0.8, 0.4, 22.4, 0.9, bg_color='#111827', border_color='#1F2937', corner_radius=0.1)

kpis_footer = [
    ("HOLDOUT MAE", "$14,761", '#10B981'),
    ("VARIANCE EXPLAINED (R²)", "89.79%", '#10B981'),
    ("PERCENT ERROR (MAPE)", "9.98%", '#34D399'),
    ("CHAMPION ARCHITECTURE", "Random Forest (Ranger)", '#A855F7'),
    ("PIPELINE DEPENDENCY", "renv.lock locked", '#60A5FA'),
    ("REGULATORY GOVERNANCE", "Non-Causal XAI Compliant", '#FBBF24')
]

x_ft = 1.1
for f_lbl, f_val, f_clr in kpis_footer:
    ax.text(x_ft, 0.95, f_lbl, color=COLOR_TEXT_DIM, fontsize=8, fontweight='bold')
    ax.text(x_ft, 0.62, f_val, color=f_clr, fontsize=12.5, fontweight='bold')
    x_ft += 3.75

# -----------------------------------------------------------------------------
# Save Outputs (PNG and JPG)
# -----------------------------------------------------------------------------
png_path = "architecture.png"
jpg_path = "architecture.jpg"

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig(png_path, dpi=DPI, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.1)
print(f"[SUCCESS] Saved high-resolution PNG: {png_path}")

# Convert to JPG using Pillow for clean compression
img_pil = Image.open(png_path)
rgb_pil = img_pil.convert('RGB')
rgb_pil.save(jpg_path, 'JPEG', quality=95)
print(f"[SUCCESS] Saved high-quality JPEG: {jpg_path}")
plt.close()
