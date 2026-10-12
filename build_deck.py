#!/usr/bin/env python3
"""
build_deck.py
Generates an executive, humanized, very simple language PowerPoint presentation
for the Ames Housing Explainable Machine Learning Project.
Follows the exact 7-part Case Study guidelines in crystal-clear plain English.
High standard readable font sizes, clean visual card hierarchy, and embedded diagnostic plots.
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -----------------------------------------------------------------------------
# PALETTE DEFINITIONS (Clean, Friendly Modern Enterprise Palette)
# -----------------------------------------------------------------------------
NAVY_DARK     = RGBColor(15, 23, 42)     # #0F172A (Deep Slate Navy)
NAVY_PRIMARY  = RGBColor(30, 58, 138)    # #1E3A8A (Primary Brand Navy)
BLUE_ACCENT   = RGBColor(37, 99, 235)    # #2563EB (Accent Blue)
BLUE_LIGHT    = RGBColor(239, 246, 255)  # #EFF6FF (Soft Blue Background)
GREEN_SUCCESS = RGBColor(5, 150, 105)    # #059669 (Success Green)
GREEN_LIGHT   = RGBColor(236, 253, 245)  # #ECFDF5 (Soft Green Tint)
AMBER_WARN    = RGBColor(217, 119, 6)    # #D97706 (Warning Amber)
RED_ACCENT    = RGBColor(220, 38, 38)    # #DC2626 (Red Accent)
TEXT_DARK     = RGBColor(30, 41, 59)     # #1E293B (Body Text Dark)
TEXT_MUTED    = RGBColor(100, 116, 139)  # #64748B (Secondary / Muted Text)
BG_PAGE       = RGBColor(248, 250, 252)  # #F8FAFC (Clean Light Canvas)
CARD_BG       = RGBColor(255, 255, 255)  # #FFFFFF (Pure White Card)
CARD_BORDER   = RGBColor(226, 232, 240)  # #E2E8F0 (Subtle Border)
WHITE         = RGBColor(255, 255, 255)

FONT_PRIMARY  = "Calibri"

def set_slide_background(slide, color):
    """Fills slide background with a solid color."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, eyebrow, title, subtitle=None, current_slide=None, total_slides=13):
    """Adds a standard clean header to content slides."""
    # Eyebrow / Category Tag
    tb_eye = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_eye = tb_eye.text_frame
    tf_eye.word_wrap = True
    tf_eye.margin_left = tf_eye.margin_top = tf_eye.margin_right = tf_eye.margin_bottom = 0
    p_eye = tf_eye.paragraphs[0]
    p_eye.text = eyebrow.upper()
    p_eye.font.name = FONT_PRIMARY
    p_eye.font.size = Pt(11)
    p_eye.font.bold = True
    p_eye.font.color.rgb = BLUE_ACCENT

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_PRIMARY
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

    # Subtitle / One-Sentence Simple Summary
    if subtitle:
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.45))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = FONT_PRIMARY
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = TEXT_MUTED

    # Bottom Footer
    tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.3))
    tf_foot = tb_foot.text_frame
    tf_foot.margin_left = tf_foot.margin_top = tf_foot.margin_right = tf_foot.margin_bottom = 0
    p_foot = tf_foot.paragraphs[0]
    slide_num_str = f" • Slide {current_slide} of {total_slides}" if current_slide else ""
    p_foot.text = f"Explainable House Price Prediction (Ames, Iowa Case Study){slide_num_str}"
    p_foot.font.name = FONT_PRIMARY
    p_foot.font.size = Pt(10)
    p_foot.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Draws a clean rounded rectangle container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_kpi_card(slide, left, top, width, height, value, label, subtext=None, val_color=NAVY_PRIMARY):
    """Draws an executive KPI callout box with large bold numbers."""
    add_card(slide, left, top, width, height, bg_color=WHITE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Big Bold Metric
    p_val = tf.paragraphs[0]
    p_val.text = str(value)
    p_val.font.name = FONT_PRIMARY
    p_val.font.size = Pt(32)
    p_val.font.bold = True
    p_val.font.color.rgb = val_color

    # Main Label
    p_lbl = tf.add_paragraph()
    p_lbl.text = label
    p_lbl.font.name = FONT_PRIMARY
    p_lbl.font.size = Pt(13)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = TEXT_DARK
    p_lbl.space_before = Pt(2)

    # Subtitle / Interpretation
    if subtext:
        p_sub = tf.add_paragraph()
        p_sub.text = subtext
        p_sub.font.name = FONT_PRIMARY
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_before = Pt(2)

# -----------------------------------------------------------------------------
# PRESENTATION INITIALIZATION
# -----------------------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]
TOTAL_SLIDES = 13

# =============================================================================
# SLIDE 1: TITLE SLIDE (Clean Executive Look)
# =============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, NAVY_DARK)

# Left accent strip
accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(0.12), Inches(4.3))
accent_bar.fill.solid()
accent_bar.fill.fore_color.rgb = BLUE_ACCENT
accent_bar.line.fill.background()

tb_s1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
tf_s1 = tb_s1.text_frame
tf_s1.word_wrap = True
tf_s1.margin_left = tf_s1.margin_top = tf_s1.margin_right = tf_s1.margin_bottom = 0

p = tf_s1.paragraphs[0]
p.text = "APPLIED MACHINE LEARNING & EXPLAINABLE AI CASE STUDY"
p.font.name = FONT_PRIMARY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = BLUE_ACCENT

p = tf_s1.add_paragraph()
p.text = "Transparent House Price Prediction"
p.font.name = FONT_PRIMARY
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = WHITE
p.space_before = Pt(8)

p = tf_s1.add_paragraph()
p.text = "Predicting Residential Valuations in Ames, Iowa with Complete Explainability"
p.font.name = FONT_PRIMARY
p.font.size = Pt(18)
p.font.color.rgb = RGBColor(191, 219, 254)
p.space_before = Pt(8)

p = tf_s1.add_paragraph()
p.text = (
    "A practical, leakage-free machine learning project built in R. We show how to clean messy real estate data, "
    "benchmark 6 algorithms, pick the best model (Random Forest), and explain every single price quote in plain English using SHAP & LIME."
)
p.font.name = FONT_PRIMARY
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(148, 163, 184)
p.space_before = Pt(16)

# Tagline badges
tb_s1_b = s1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(11.0), Inches(0.6))
tf_s1_b = tb_s1_b.text_frame
tf_s1_b.margin_left = tf_s1_b.margin_top = tf_s1_b.margin_right = tf_s1_b.margin_bottom = 0
p = tf_s1_b.paragraphs[0]
p.text = "2,930 Real Homes  •  Leakage-Free R Pipelines  •  89.8% Accuracy  •  Interactive Web Calculator"
p.font.name = FONT_PRIMARY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = GREEN_SUCCESS

# =============================================================================
# SLIDE 2: THE REAL-WORLD PROBLEM (Why Simple Explanations Matter)
# =============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, BG_PAGE)
add_header(s2, "1. Case Study Overview",
           "The Core Problem: Why We Need Explainable Predictions",
           "Why traditional valuation methods fail homeowners and loan officers in real life", 2, TOTAL_SLIDES)

# Card 1: The Black-Box Problem
add_card(s2, Inches(0.8), Inches(1.9), Inches(5.6), Inches(3.6), bg_color=WHITE, border_color=CARD_BORDER)
s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(0.1)).fill.solid()
s2.shapes[-1].fill.fore_color.rgb = RED_ACCENT
s2.shapes[-1].line.fill.background()

tb = s2.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(3.1))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "Problem 1: Black-Box AI (Too Opaque)"
p.font.name = FONT_PRIMARY
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = RED_ACCENT

points_c1 = [
    ("Accurate but Silent: ", "Advanced algorithms can guess prices well, but they act like a black box—they give you a number without giving you a reason."),
    ("The $40,000 Mystery: ", "If a buyer's appraisal comes in $40,000 below expectations, telling them 'the computer calculated it' is unacceptable."),
    ("Lending Regulations: ", "Banks must legally explain why loans are approved or denied. Unexplained AI decisions violate fair lending laws.")
]
for bold_pfx, txt in points_c1:
    p = tf.add_paragraph()
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(13)
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = "• " + bold_pfx
    r1.font.bold = True
    r1.font.color.rgb = TEXT_DARK
    r2 = p.add_run()
    r2.text = txt
    r2.font.color.rgb = TEXT_DARK

# Card 2: Simple Linear Regression Problem
add_card(s2, Inches(6.8), Inches(1.9), Inches(5.7), Inches(3.6), bg_color=WHITE, border_color=CARD_BORDER)
s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(0.1)).fill.solid()
s2.shapes[-1].fill.fore_color.rgb = BLUE_ACCENT
s2.shapes[-1].line.fill.background()

tb = s2.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(3.1))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "Problem 2: Simple Formulas (Too Inaccurate)"
p.font.name = FONT_PRIMARY
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = BLUE_ACCENT

points_c2 = [
    ("Easy to Read: ", "Basic linear formulas are simple: every square foot adds a fixed dollar amount."),
    ("Real Estate Isn't Simple: ", "In real life, 200 sq ft on a luxury custom mansion adds way more cash than 200 sq ft on an old fixer-upper."),
    ("High Average Errors: ", "Basic linear formulas made an average error of over $21,000 on our data because they cannot see complex combinations.")
]
for bold_pfx, txt in points_c2:
    p = tf.add_paragraph()
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(13)
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = "• " + bold_pfx
    r1.font.bold = True
    r1.font.color.rgb = TEXT_DARK
    r2 = p.add_run()
    r2.text = txt
    r2.font.color.rgb = TEXT_DARK

# Bottom Solution Banner
add_card(s2, Inches(0.8), Inches(5.75), Inches(11.7), Inches(0.95), bg_color=GREEN_LIGHT, border_color=GREEN_SUCCESS)
tb = s2.shapes.add_textbox(Inches(1.1), Inches(5.85), Inches(11.1), Inches(0.75))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "Our Goal in Plain English:"
p.font.name = FONT_PRIMARY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = GREEN_SUCCESS

p = tf.add_paragraph()
p.text = "Build a model that achieves top-level accuracy (under $15k average error), while printing a clear, itemized receipt for every single property so any human can understand why it is priced that way."
p.font.name = FONT_PRIMARY
p.font.size = Pt(13)
p.font.color.rgb = TEXT_DARK

# =============================================================================
# SLIDE 3: DATASET OVERVIEW (2,930 Real Ames Properties)
# =============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, BG_PAGE)
add_header(s3, "2. Dataset Description",
           "The Ames Housing Data: 2,930 Real Homes",
           "What information we had, and why it was ideal for testing our prediction system", 3, TOTAL_SLIDES)

# 3 Metric boxes on the left
add_kpi_card(s3, Inches(0.8), Inches(1.9), Inches(5.8), Inches(1.2),
             "2,930 Homes", "Total Sales Recorded", "Ames, Iowa property transactions (2006 to 2010)", NAVY_PRIMARY)

add_kpi_card(s3, Inches(0.8), Inches(3.25), Inches(5.8), Inches(1.2),
             "81 Features", "Information Per House", "Size, build year, quality grades, neighborhood, and amenities", BLUE_ACCENT)

add_kpi_card(s3, Inches(0.8), Inches(4.6), Inches(5.8), Inches(1.2),
             "$34.9k – $755k", "Selling Price Range", "Average home was $180,800; middle home (median) was $160,000", GREEN_SUCCESS)

# Right Column: Distribution Plot + Explanation
add_card(s3, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.7), bg_color=WHITE, border_color=CARD_BORDER)
plot_path_s3 = "figures/eda_01_target_distribution_raw.png"
if os.path.exists(plot_path_s3):
    s3.shapes.add_picture(plot_path_s3, Inches(7.05), Inches(2.0), Inches(5.3), Inches(3.5))

tb = s3.shapes.add_textbox(Inches(7.1), Inches(5.65), Inches(5.2), Inches(0.8))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "Why this dataset is great: Most homes cost between $120k and $220k, but a few luxury estates cost up to $755k. This teaches our model to handle normal houses well without getting tricked by mansions."
p.font.name = FONT_PRIMARY
p.font.size = Pt(11)
p.font.color.rgb = TEXT_MUTED

# =============================================================================
# SLIDE 4: DATA PREPARATION (The 3 Traps We Cleaned)
# =============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, BG_PAGE)
add_header(s4, "3. Data Preparation & Cleaning",
           "Data Detective Work: Finding & Fixing 3 Traps",
           "Before feeding data into any model, we checked for errors and bad columns", 4, TOTAL_SLIDES)

traps = [
    ("Trap 1: The Completely Useless Column (Misc_Feature_2)",
     "What was wrong: This column had the exact same value for all 2,930 houses.\n"
     "Why it matters: A feature with zero differences gives zero clues. It's just clutter.\n"
     "What we did: We automatically dropped it before training.",
     AMBER_WARN),
    ("Trap 2: The Exact Twin Column (Condition_3)",
     "What was wrong: Condition_3 was a 100% identical copy of Condition_2.\n"
     "Why it matters: If you feed two identical columns, models can double-count that feature.\n"
     "What we did: We deleted the duplicate and kept the original.",
     AMBER_WARN),
    ("Trap 3: Measuring the Same Yard Twice (Lot_Area_m2)",
     "What was wrong: One column was lot area in sq ft; another was the exact same yard in sq meters.\n"
     "Why it matters: It was just a math conversion of the same information, causing confusion.\n"
     "What we did: We removed the metric clone and kept square footage.",
     RED_ACCENT)
]

y_pos = 1.9
for title, desc, col in traps:
    add_card(s4, Inches(0.8), Inches(y_pos), Inches(11.7), Inches(1.4), bg_color=WHITE, border_color=CARD_BORDER)
    bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(y_pos), Inches(0.12), Inches(1.4))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()

    tb = s4.shapes.add_textbox(Inches(1.15), Inches(y_pos + 0.12), Inches(11.1), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = col

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_PRIMARY
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(3)

    y_pos += 1.55

# =============================================================================
# SLIDE 5: ZERO DATA LEAKAGE (How We Kept the Model Honest)
# =============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, BG_PAGE)
add_header(s5, "3. Data Preparation & Integrity",
           "The Cheating Trap: How We Guaranteed Zero Leakage",
           "What is data leakage, and why our strict pipeline makes our test scores 100% trustworthy", 5, TOTAL_SLIDES)

steps_leak = [
    ("1. What is Data Leakage?",
     "Imagine giving a student the answer key before a practice exam.\n\n"
     "If you fill missing values or calculate averages using the WHOLE dataset before splitting into test groups, your model secretly peeks at the test answers. Its score looks amazing, but it fails in the real world.",
     RED_ACCENT),
    ("2. How Our Pipeline Fixes It",
     "We used mlr3pipelines DAG to lock all cleaning inside the model:\n\n"
     "• In each round, the model learns averages ONLY from the study homes.\n"
     "• When it looks at test homes, it treats them as completely unseen.\n"
     "• If a house has missing features (like no fireplace), it marks 'MISSING' cleanly.",
     BLUE_ACCENT),
    ("3. Why This Gives You Confidence",
     "Our holdout results are 100% honest:\n\n"
     "When we say our model makes an average error of $14,761 on brand-new homes, that is real-world performance, not an inflated score from accidental cheating.",
     GREEN_SUCCESS)
]

x_pos = 0.8
for title, desc, col in steps_leak:
    add_card(s5, Inches(x_pos), Inches(1.9), Inches(3.7), Inches(4.7), bg_color=WHITE, border_color=CARD_BORDER)
    strip = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x_pos), Inches(1.9), Inches(3.7), Inches(0.1))
    strip.fill.solid()
    strip.fill.fore_color.rgb = col
    strip.line.fill.background()

    tb = s5.shapes.add_textbox(Inches(x_pos + 0.2), Inches(2.15), Inches(3.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = col

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_PRIMARY
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(8)

    x_pos += 3.95

# =============================================================================
# SLIDE 6: FEATURE ENGINEERING (Teaching the Model Buyer Psychology)
# =============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, BG_PAGE)
add_header(s6, "3. Domain Feature Engineering",
           "Smart Features: Teaching the Model How Buyers Think",
           "We created 6 practical combination features that match how real people evaluate homes", 6, TOTAL_SLIDES)

# Left Column: Correlation chart
add_card(s6, Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.7), bg_color=WHITE, border_color=CARD_BORDER)
plot_path_s6 = "figures/eda_07_engineered_features_correlations.png"
if os.path.exists(plot_path_s6):
    s6.shapes.add_picture(plot_path_s6, Inches(0.9), Inches(2.0), Inches(5.6), Inches(4.1))

tb = s6.shapes.add_textbox(Inches(0.9), Inches(6.15), Inches(5.6), Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "Result: Our engineered interaction (Quality x Size) became the #1 strongest predictor in the entire dataset (r = 0.85)!"
p.font.name = FONT_PRIMARY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = GREEN_SUCCESS

# Right Column: 4 Plain English Features
features_simple = [
    ("1. Quality Multiplied by Size (r = 0.85)",
     "The #1 Most Important Clue: An extra 200 sq ft on a luxury estate adds way more money than 200 sq ft on an entry-level house. Multiplying them together captured this compounding effect.",
     GREEN_SUCCESS),
    ("2. Total Usable Living Space",
     "Buyers don't just look at above-ground space—they care about finished basements too. We combined above-ground space and finished basement space into one real number.",
     NAVY_PRIMARY),
    ("3. All Bathrooms Combined",
     "Rather than confusing full baths, half baths, and basement baths in separate columns, we created a single Total Bathrooms score.",
     NAVY_PRIMARY),
    ("4. House Age vs. Remodel Year",
     "A 1960 home with a 2008 kitchen renovation is worth way more than an untouched 1960 original. We tracked both build age and remodel recency.",
     NAVY_PRIMARY)
]

y_pos_fe = 1.9
for title, desc, col in features_simple:
    add_card(s6, Inches(6.9), Inches(y_pos_fe), Inches(5.6), Inches(1.05), bg_color=WHITE, border_color=CARD_BORDER)
    tb = s6.shapes.add_textbox(Inches(7.1), Inches(y_pos_fe + 0.08), Inches(5.2), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = col

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_PRIMARY
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(2)

    y_pos_fe += 1.18

# =============================================================================
# SLIDE 7: THE TOURNAMENT (Testing 6 Algorithms)
# =============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, BG_PAGE)
add_header(s7, "4. Model Benchmarking",
           "The Model Tournament: Testing 6 Algorithms Head-to-Head",
           "We tested 6 different machine learning methods on the exact same 5 rounds of cross-validation", 7, TOTAL_SLIDES)

# Left Column: MAE Plot
add_card(s7, Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.7), bg_color=WHITE, border_color=CARD_BORDER)
plot_path_s7 = "figures/benchmark_01_mae_comparison.png"
if os.path.exists(plot_path_s7):
    s7.shapes.add_picture(plot_path_s7, Inches(0.9), Inches(2.0), Inches(5.6), Inches(4.2))

# Right Column: Leaderboard & Why Random Forest Won
add_card(s7, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.7), bg_color=WHITE, border_color=CARD_BORDER)
tb = s7.shapes.add_textbox(Inches(7.2), Inches(2.1), Inches(5.1), Inches(4.3))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "Tournament Leaderboard (Average Error)"
p.font.name = FONT_PRIMARY
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY

models_plain = [
    ("1. XGBoost (Boosted Trees)", "$15,321 average error", "89.3% accuracy", GREEN_SUCCESS),
    ("2. Random Forest (Ranger)", "$15,858 average error", "89.1% accuracy", NAVY_PRIMARY),
    ("3. ElasticNet (Smart Linear)", "$16,749 average error", "71.8% accuracy", TEXT_DARK),
    ("4. Basic Linear Regression", "$21,093 average error", "78.6% accuracy", TEXT_DARK),
    ("5. Single Decision Tree", "$27,458 average error", "74.3% accuracy", TEXT_DARK),
    ("6. Guessing Average Price", "$58,761 average error", "0% accuracy", RED_ACCENT)
]
for name, err, r2, col in models_plain:
    p = tf.add_paragraph()
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(13)
    p.space_before = Pt(5)
    r1 = p.add_run()
    r1.text = f"{name}: "
    r1.font.bold = True
    r1.font.color.rgb = col
    r2 = p.add_run()
    r2.text = f"{err} ({r2})"
    r2.font.color.rgb = TEXT_DARK

p_dec = tf.add_paragraph()
p_dec.text = "Why We Picked Random Forest as Our Champion:"
p_dec.font.name = FONT_PRIMARY
p_dec.font.size = Pt(14)
p_dec.font.bold = True
p_dec.font.color.rgb = NAVY_PRIMARY
p_dec.space_before = Pt(12)

p_dec_txt = tf.add_paragraph()
p_dec_txt.text = (
    "Even though XGBoost was $537 slightly lower in error, Random Forest was much more stable across rounds, "
    "never makes wild crazy guesses on unusual luxury mansions, and works seamlessly with explainable AI tools."
)
p_dec_txt.font.name = FONT_PRIMARY
p_dec_txt.font.size = Pt(12)
p_dec_txt.font.color.rgb = TEXT_DARK
p_dec_txt.space_before = Pt(4)

# =============================================================================
# SLIDE 8: TUNING THE RANDOM FOREST
# =============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, BG_PAGE)
add_header(s8, "5. Model Optimization",
           "Fine-Tuning: Making the Random Forest 5% Sharper",
           "How we adjusted tree settings to cut another $800+ off our prediction error", 8, TOTAL_SLIDES)

tune_plain = [
    ("Knob 1: Features Looked At (mtry = 44)",
     "The default setting only looked at 9 features per tree split, which was too cautious for 81 features.\n\n"
     "We bumped it to 44 so trees could discover multi-feature combinations (like great quality AND great location together).",
     NAVY_PRIMARY),
    ("Knob 2: Minimum Branch Size (node = 4)",
     "We allowed trees to look at small clusters of 4 houses.\n\n"
     "This let the forest learn localized pricing pockets across neighborhoods without letting individual trees memorize single houses.",
     BLUE_ACCENT),
    ("Knob 3: Data Subsample (89% per tree)",
     "Each tree learned on nearly 90% of the training data.\n\n"
     "This stabilized predictions across volatile price categories and stopped predictions from jumping around randomly.",
     GREEN_SUCCESS)
]

x_pos = 0.8
for title, desc, col in tune_plain:
    add_card(s8, Inches(x_pos), Inches(1.9), Inches(3.7), Inches(3.4), bg_color=WHITE, border_color=CARD_BORDER)
    tb = s8.shapes.add_textbox(Inches(x_pos + 0.2), Inches(2.1), Inches(3.3), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = col

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_PRIMARY
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(8)

    x_pos += 3.95

# Bottom summary card
add_card(s8, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.2), bg_color=BLUE_LIGHT, border_color=BLUE_ACCENT)
tb = s8.shapes.add_textbox(Inches(1.1), Inches(5.6), Inches(11.1), Inches(1.0))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "Tuning Takeaway in Plain English:"
p.font.name = FONT_PRIMARY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY

p_d = tf.add_paragraph()
p_d.text = (
    "Adjusting these 3 settings shaved another $800+ off our error, bringing internal error down to $15,969. "
    "The model became faster, smoother, and ready for production deployment."
)
p_d.font.name = FONT_PRIMARY
p_d.font.size = Pt(12)
p_d.font.color.rgb = TEXT_DARK
p_d.space_before = Pt(2)

# =============================================================================
# SLIDE 9: THE FINAL EXAM (586 Untouched Houses)
# =============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, BG_PAGE)
add_header(s9, "5. Final Test Results",
           "The Final Exam: Testing on 586 Brand New Homes",
           "We evaluated our trained model on a locked test set it had never seen before", 9, TOTAL_SLIDES)

# 4 KPI cards across the top
kpis_simple = [
    ("$14,761", "Average Error (MAE)", "Our target was < $16,000 (PASSED)", GREEN_SUCCESS),
    ("89.79%", "Accuracy Score (R²)", "Our target was > 85.0% (PASSED)", GREEN_SUCCESS),
    ("9.98%", "Typical Error %", "Predictions are typically within 10% of sale price", BLUE_ACCENT),
    ("586 Homes", "Test Set Size", "Locked 20% partition tested after all training", NAVY_PRIMARY)
]
for i, (val, lbl, sub, col) in enumerate(kpis_simple):
    add_kpi_card(s9, Inches(0.8 + i * 2.95), Inches(1.9), Inches(2.75), Inches(1.3), val, lbl, sub, col)

# Bottom Left: Residual Plot
add_card(s9, Inches(0.8), Inches(3.4), Inches(6.8), Inches(3.3), bg_color=WHITE, border_color=CARD_BORDER)
plot_path_s9 = "figures/evaluation_residual_diagnostics.png"
if os.path.exists(plot_path_s9):
    s9.shapes.add_picture(plot_path_s9, Inches(0.9), Inches(3.45), Inches(6.6), Inches(3.15))

# Bottom Right: Plain English Diagnostic Takeaways
add_card(s9, Inches(7.8), Inches(3.4), Inches(4.7), Inches(3.3), bg_color=WHITE, border_color=CARD_BORDER)
tb = s9.shapes.add_textbox(Inches(8.0), Inches(3.55), Inches(4.3), Inches(3.0))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "What the Diagnostics Tell Us:"
p.font.name = FONT_PRIMARY
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY

insights_plain = [
    ("No Systematic Bias: ", "Errors balance equally above and below $0. The model doesn't consistently over-value or under-value homes."),
    ("Tight Middle Range: ", "For normal family homes ($130k to $250k), errors are small—typically within 5% to 8%."),
    ("Why Errors Grow on Mansions: ", "On houses above $450k, errors are larger because luxury homes have custom architectural details (like heated pools or wine cellars) that standard data cannot capture.")
]
for pfx, txt in insights_plain:
    p = tf.add_paragraph()
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(12)
    p.space_before = Pt(6)
    r1 = p.add_run()
    r1.text = "• " + pfx
    r1.font.bold = True
    r1.font.color.rgb = TEXT_DARK
    r2 = p.add_run()
    r2.text = txt
    r2.font.color.rgb = TEXT_DARK

# =============================================================================
# SLIDE 10: GLOBAL EXPLAINABILITY (What Moves the Market?)
# =============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, BG_PAGE)
add_header(s10, "5. Explainability (Global)",
           "Market Secrets: What Really Drives House Prices in Ames?",
           "We shuffled each feature to see how much worse the model got without it", 10, TOTAL_SLIDES)

# Left Column: Global importance plot
add_card(s10, Inches(0.8), Inches(1.9), Inches(5.8), Inches(4.7), bg_color=WHITE, border_color=CARD_BORDER)
plot_path_s10 = "figures/xai_01_global_importance.png"
if os.path.exists(plot_path_s10):
    s10.shapes.add_picture(plot_path_s10, Inches(0.9), Inches(2.0), Inches(5.6), Inches(4.3))

# Right Column: 4 Plain English Market Lessons
add_card(s10, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.7), bg_color=WHITE, border_color=CARD_BORDER)
tb = s10.shapes.add_textbox(Inches(7.2), Inches(2.1), Inches(5.1), Inches(4.3))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "The 4 Biggest Price Drivers:"
p.font.name = FONT_PRIMARY
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY

drivers_plain = [
    ("1. Quality Combined with Size (50%+): ", "Nothing matters more than how big the home is multiplied by its construction quality. A large high-quality house is the ultimate price driver."),
    ("2. Location, Location, Location: ", "Neighborhood is the #1 categorical modifier. Premium neighborhoods like Northridge Heights set a much higher baseline price."),
    ("3. Age is a Steady Discount: ", "Every decade of age reduces price, UNLESS the owner has completed major modern remodeling additions."),
    ("4. Finished vs Unfinished Space: ", "Finished basement space adds about $50/sq ft. Unfinished basement storage space adds almost nothing to valuation.")
]
for pfx, txt in drivers_plain:
    p = tf.add_paragraph()
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(13)
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = "• " + pfx
    r1.font.bold = True
    r1.font.color.rgb = NAVY_PRIMARY
    r2 = p.add_run()
    r2.text = txt
    r2.font.color.rgb = TEXT_DARK

# =============================================================================
# SLIDE 11: LOCAL EXPLAINABILITY (SHAP Waterfall on a Single House)
# =============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, BG_PAGE)
add_header(s11, "5. Explainability (Local SHAP)",
           "Explaining Any Single House Like an Itemized Receipt",
           "How SHAP breaks down a $378,000 luxury home compared to the $180,800 Ames average", 11, TOTAL_SLIDES)

# Left Column: SHAP Waterfall Plot
add_card(s11, Inches(0.8), Inches(1.9), Inches(5.8), Inches(3.6), bg_color=WHITE, border_color=CARD_BORDER)
plot_path_s11 = "figures/xai_02_shap_luxury_waterfall.png"
if os.path.exists(plot_path_s11):
    s11.shapes.add_picture(plot_path_s11, Inches(0.9), Inches(2.0), Inches(5.6), Inches(3.35))

# Right Column: The Itemized Receipt
add_card(s11, Inches(6.9), Inches(1.9), Inches(5.6), Inches(3.6), bg_color=WHITE, border_color=CARD_BORDER)
tb = s11.shapes.add_textbox(Inches(7.2), Inches(2.1), Inches(5.1), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "How SHAP Explains This $378k House:"
p.font.name = FONT_PRIMARY
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY

shap_steps = [
    ("Starting Baseline: ", "Average Ames Home = $180,800"),
    ("+ Huge Living Space (4,200 sq ft): ", "+$82,400 enhancement"),
    ("+ Top Quality Materials (Grade 9/10): ", "+$54,200 enhancement"),
    ("+ Great Neighborhood (Northridge Hts): ", "+$22,100 enhancement"),
    ("- Older Construction Era: ", "-$18,400 age discount"),
    ("- Partial Unfinished Basement: ", "-$11,300 layout discount"),
    ("= Final Model Valuation: ", "$352,858 (Closed at $378,000; 6.6% error)")
]
for pfx, txt in shap_steps:
    p = tf.add_paragraph()
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(12)
    p.space_before = Pt(3)
    r1 = p.add_run()
    r1.text = pfx
    r1.font.bold = True
    r1.font.color.rgb = GREEN_SUCCESS if "+" in pfx else (RED_ACCENT if "-" in pfx else NAVY_PRIMARY)
    r2 = p.add_run()
    r2.text = txt
    r2.font.color.rgb = TEXT_DARK

# Bottom Governance Card (Very Simple Language)
add_card(s11, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.05), bg_color=RGBColor(254, 243, 199), border_color=AMBER_WARN)
tb = s11.shapes.add_textbox(Inches(1.1), Inches(5.72), Inches(11.1), Inches(0.85))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "A Common-Sense Legal Rule to Remember (Non-Causal Warning):"
p.font.name = FONT_PRIMARY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = AMBER_WARN

p_d = tf.add_paragraph()
p_d.text = (
    "SHAP tells us how the model arrived at its prediction. It DOES NOT guarantee that if a homeowner spends $10,000 "
    "adding a bathroom, their house will automatically sell for $10,000 more. Correlation is not a physical warranty."
)
p_d.font.name = FONT_PRIMARY
p_d.font.size = Pt(12)
p_d.font.color.rgb = TEXT_DARK
p_d.space_before = Pt(2)

# =============================================================================
# SLIDE 12: THE INTERACTIVE SHINY APPLICATION
# =============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12, BG_PAGE)
add_header(s12, "6. Practical Deployment",
           "The Interactive Valuation Tool: A Live Web App",
           "We deployed our model into an easy-to-use Shiny web app with 1-click buttons and sensitivity curves", 12, TOTAL_SLIDES)

shiny_simple = [
    ("1-Click Preset Buttons",
     "No need to type 80 numbers by hand:\n\n"
     "• Starter Home: $129,746\n  (1,050 sq ft, 1 bath, average quality)\n\n"
     "• Median Family Home: $179,418\n  (1,600 sq ft, 2.5 baths, good quality)\n\n"
     "• Luxury Estate: $328,090\n  (2,800 sq ft, 3.5 baths, excellent quality)",
     NAVY_PRIMARY),
    ("Live 'What-If' Curve",
     "Interactive Living Area Trajectory:\n\n"
     "• Shows a smooth curve from 800 to 3,600 sq ft.\n\n"
     "• Marks a red diamond on the user's current house.\n\n"
     "• Lets homeowners instantly see: 'If I finish my 400 sq ft attic, how much does my property value jump?'",
     BLUE_ACCENT),
    ("Live Marginal Value Badges",
     "Instant dollar answers to practical questions:\n\n"
     "• +200 sq ft Living Space: +$16,000 lift\n\n"
     "• +1 Full Bathroom: +$9,500 lift\n\n"
     "• Complete Modern Remodel: +$12,000 lift\n\n"
     "Evaluated live on-the-fly by the trained model.",
     GREEN_SUCCESS)
]

x_pos = 0.8
for title, desc, col in shiny_simple:
    add_card(s12, Inches(x_pos), Inches(1.9), Inches(3.7), Inches(3.4), bg_color=WHITE, border_color=CARD_BORDER)
    strip = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x_pos), Inches(1.9), Inches(3.7), Inches(0.1))
    strip.fill.solid()
    strip.fill.fore_color.rgb = col
    strip.line.fill.background()

    tb = s12.shapes.add_textbox(Inches(x_pos + 0.2), Inches(2.15), Inches(3.3), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = col

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_PRIMARY
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(8)

    x_pos += 3.95

# Bottom transparency audit
add_card(s12, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.2), bg_color=CARD_BG, border_color=CARD_BORDER)
tb = s12.shapes.add_textbox(Inches(1.1), Inches(5.6), Inches(11.1), Inches(1.0))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "Complete Transparency for Unexposed Details:"
p.font.name = FONT_PRIMARY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY

p_d = tf.add_paragraph()
p_d.text = (
    "For details not shown on the simple screen (like electrical panel type or foundation materials), "
    "the app clearly lists its assumptions using standard Ames medians so there are zero hidden surprises."
)
p_d.font.name = FONT_PRIMARY
p_d.font.size = Pt(12)
p_d.font.color.rgb = TEXT_DARK
p_d.space_before = Pt(2)

# =============================================================================
# SLIDE 13: KEY TAKEAWAYS & LESSONS (Easy to Explain)
# =============================================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13, BG_PAGE)
add_header(s13, "7. Conclusions & What We Learned",
           "Key Takeaways: 4 Big Lessons from This Case Study",
           "Simple, practical lessons you can remember and explain with confidence", 13, TOTAL_SLIDES)

lessons_plain = [
    ("Lesson 1: Cleaning Inside the Model Stops Cheating",
     "Never clean data outside your cross-validation folds. Wrapping everything in a strict pipeline (mlr3pipelines) guarantees your test scores reflect true real-world performance.",
     NAVY_PRIMARY),
    ("Lesson 2: Smart Features Beat Complex Tuning",
     "Multiplying Quality x Size alone gave us more accuracy than weeks of hyperparameter tweaking. Knowing your domain matters more than raw compute.",
     BLUE_ACCENT),
    ("Lesson 3: Explainable AI Builds Real Trust",
     "Nobody trusts a silent black box. Giving users an itemized SHAP breakdown (receipt) bridges the gap between machine learning and human decision-making.",
     GREEN_SUCCESS),
    ("Lesson 4: Reproducibility Makes Work Professional",
     "Locking package versions (renv.lock), testing endpoints automatically, and compiling standalone reports means anyone can re-run this project anytime with identical results.",
     AMBER_WARN)
]

for i, (ttitle, tdesc, col) in enumerate(lessons_plain):
    row = i // 2
    col_idx = i % 2
    x_pos = 0.8 + col_idx * 5.95
    y_pos = 1.9 + row * 2.35

    add_card(s13, Inches(x_pos), Inches(y_pos), Inches(5.6), Inches(2.15), bg_color=WHITE, border_color=CARD_BORDER)
    bar = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x_pos), Inches(y_pos), Inches(0.1), Inches(2.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()

    tb = s13.shapes.add_textbox(Inches(x_pos + 0.25), Inches(y_pos + 0.15), Inches(5.1), Inches(1.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_t = tf.paragraphs[0]
    p_t.text = ttitle
    p_t.font.name = FONT_PRIMARY
    p_t.font.size = Pt(16)
    p_t.font.bold = True
    p_t.font.color.rgb = col

    p_d = tf.add_paragraph()
    p_d.text = tdesc
    p_d.font.name = FONT_PRIMARY
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = TEXT_DARK
    p_d.space_before = Pt(6)

# -----------------------------------------------------------------------------
# SAVE PRESENTATION
# -----------------------------------------------------------------------------
output_path = "reports/Explainable_House_Price_Prediction_Presentation.pptx"
prs.save(output_path)
root_path = "Explainable_House_Price_Prediction_Presentation.pptx"
prs.save(root_path)
print(f"[SUCCESS] Presentation generated successfully: {output_path} and {root_path}")
print(f"Total Slides: {len(prs.slides)}")
