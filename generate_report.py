"""
generate_report.py
------------------
Generates Nepal_Flood_Risk_Project_Report.pdf
Run from the project root:
    python generate_report.py
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#0f172a")
BLUE       = colors.HexColor("#1d4ed8")
BLUE_LIGHT = colors.HexColor("#eff6ff")
BLUE_BRD   = colors.HexColor("#bfdbfe")
SLATE      = colors.HexColor("#475569")
MUTED      = colors.HexColor("#94a3b8")
BORDER     = colors.HexColor("#e2e8f0")
BG_CARD    = colors.HexColor("#f8fafc")
C_LOW      = colors.HexColor("#16a34a")
C_MED      = colors.HexColor("#d97706")
C_HIGH     = colors.HexColor("#dc2626")
BG_LOW     = colors.HexColor("#f0fdf4")
BG_MED     = colors.HexColor("#fffbeb")
BG_HIGH    = colors.HexColor("#fef2f2")
WHITE      = colors.white
BLACK      = colors.HexColor("#1f2328")

W, H = A4
MARGIN = 2.0 * cm

# ── Style sheet ───────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S("cover_title",
    fontSize=26, fontName="Helvetica-Bold", textColor=NAVY,
    alignment=TA_CENTER, spaceAfter=8, leading=30)

cover_sub = S("cover_sub",
    fontSize=12, fontName="Helvetica", textColor=SLATE,
    alignment=TA_CENTER, spaceAfter=6)

cover_badge = S("cover_badge",
    fontSize=9, fontName="Helvetica-Bold", textColor=BLUE,
    alignment=TA_CENTER, spaceAfter=14)

h1 = S("h1",
    fontSize=15, fontName="Helvetica-Bold", textColor=NAVY,
    spaceBefore=22, spaceAfter=8, borderPad=4,
    borderColor=BLUE, borderWidth=0, leftIndent=10)

h2 = S("h2",
    fontSize=12, fontName="Helvetica-Bold", textColor=NAVY,
    spaceBefore=14, spaceAfter=6)

body = S("body",
    fontSize=9.5, fontName="Helvetica", textColor=BLACK,
    leading=15, spaceAfter=5, alignment=TA_JUSTIFY)

bullet = S("bullet",
    fontSize=9.5, fontName="Helvetica", textColor=BLACK,
    leading=14, leftIndent=14, spaceAfter=3,
    bulletIndent=6, bulletFontName="Helvetica")

caption_s = S("caption_s",
    fontSize=8, fontName="Helvetica-Oblique", textColor=MUTED,
    spaceAfter=8, alignment=TA_CENTER)

info_s = S("info_s",
    fontSize=9, fontName="Helvetica", textColor=colors.HexColor("#1e3a8a"),
    leading=14, leftIndent=10, rightIndent=10, spaceAfter=6)

toc_s = S("toc_s",
    fontSize=9.5, fontName="Helvetica", textColor=BLACK, leading=16)

footer_s = S("footer_s",
    fontSize=8, fontName="Helvetica", textColor=MUTED,
    alignment=TA_CENTER)

# ── Table helpers ─────────────────────────────────────────────────────────────
TBL_HDR = TableStyle([
    ("BACKGROUND", (0,0), (-1,0), BLUE),
    ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,0), 8),
    ("ALIGN",      (0,0), (-1,0), "LEFT"),
    ("BOTTOMPADDING", (0,0), (-1,0), 7),
    ("TOPPADDING",    (0,0), (-1,0), 7),
    ("FONTNAME",   (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",   (0,1), (-1,-1), 8.5),
    ("ALIGN",      (0,1), (-1,-1), "LEFT"),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,1), (-1,-1), 5),
    ("BOTTOMPADDING", (0,1), (-1,-1), 5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, BG_CARD]),
    ("GRID",       (0,0), (-1,-1), 0.4, BORDER),
    ("LINEBELOW",  (0,0), (-1,0), 1.2, BLUE),
])

def table(data, col_widths, style=None, extra=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    ts = TableStyle(TBL_HDR.getCommands())
    if style:
        for cmd in style:
            ts.add(*cmd)
    if extra:
        for cmd in extra:
            ts.add(*cmd)
    t.setStyle(ts)
    return t

def info_box(text):
    data = [[Paragraph(text, info_s)]]
    t = Table(data, colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BLUE_LIGHT),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0), (-1,-1), 10),
        ("LINEAFTER", (0,0), (0,-1), 3, BLUE),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t

def warn_box(text):
    ws = ParagraphStyle("ws", fontSize=9, fontName="Helvetica",
        textColor=colors.HexColor("#92400e"), leading=14,
        leftIndent=10, rightIndent=10)
    data = [[Paragraph(text, ws)]]
    t = Table(data, colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BG_MED),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("LINEAFTER", (0,0), (0,-1), 3, C_MED),
    ]))
    return t

def section_rule():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6, spaceBefore=2)

def bar_table(rows):
    """rows = [(label, pct_str, width_0_to_1), ...]"""
    usable = W - 2*MARGIN
    col1 = usable * 0.38
    col2 = usable * 0.47
    col3 = usable * 0.15

    data = [["Feature", "Importance", "%"]]
    for label, pct_str, width in rows:
        d = Drawing(col2 * 0.95, 10)
        d.add(Rect(0, 1, col2 * 0.95, 8, fillColor=colors.HexColor("#f1f5f9"), strokeColor=None))
        d.add(Rect(0, 1, col2 * 0.95 * width, 8, fillColor=BLUE, strokeColor=None))
        data.append([label, d, pct_str])

    t = Table(data, colWidths=[col1, col2, col3])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8.5),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("ALIGN",         (2,0), (2,-1), "RIGHT"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, BG_CARD]),
        ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
        ("LINEBELOW",     (0,0), (-1,0), 1.2, BLUE),
    ]))
    return t

# ── Page template with page numbers ──────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, H - 0.7*cm, "Nepal Flood Risk Prediction & Early Warning System")
    canvas.drawRightString(W - MARGIN, H - 0.7*cm, "Technical Project Report")
    # Footer
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(W/2, 0.7*cm, f"Page {doc.page}")
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.1*cm, W - MARGIN, 1.1*cm)
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
    canvas.restoreState()

# ── Build content ─────────────────────────────────────────────────────────────
def build():
    out = os.path.join(os.path.dirname(__file__), "Nepal_Flood_Risk_Project_Report.pdf")
    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.8*cm, bottomMargin=1.6*cm,
        title="Nepal Flood Risk Prediction — Project Report",
        author="Nepal Flood Intelligence System",
    )

    story = []
    P = Paragraph
    SP = Spacer

    # ══════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(SP(1, 2.5*cm))
    story.append(P("TECHNICAL PROJECT REPORT", cover_badge))
    story.append(SP(1, 0.3*cm))
    story.append(P("Nepal Flood Risk Prediction<br/>&amp; Early Warning System", cover_title))
    story.append(SP(1, 0.2*cm))
    story.append(P("AI-Powered Flood Intelligence Platform using Machine Learning", cover_sub))
    story.append(SP(1, 1.2*cm))

    # Cover KPI table
    cov_data = [
        ["Dataset", "Nepal Flood & Weather 2023–2026 (Kaggle)"],
        ["Problem Type", "Multi-class Classification (3 classes)"],
        ["Best Model", "Random Forest Classifier"],
        ["Weighted F1 Score", "87.65%"],
        ["ROC-AUC", "0.9788"],
        ["Training Records", "10,712"],
        ["Test Records", "2,678"],
        ["Total Features", "31 (14 base + 17 engineered)"],
        ["Platform", "Python · scikit-learn · Streamlit · Plotly"],
    ]
    ct = Table(cov_data, colWidths=[(W-2*MARGIN)*0.42, (W-2*MARGIN)*0.58])
    ct.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",  (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",  (0,0), (-1,-1), 10),
        ("TEXTCOLOR", (0,0), (0,-1), NAVY),
        ("TEXTCOLOR", (1,0), (1,-1), SLATE),
        ("ALIGN",     (0,0), (-1,-1), "LEFT"),
        ("VALIGN",    (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[BLUE_LIGHT, WHITE]),
        ("BOX",       (0,0), (-1,-1), 1, BLUE_BRD),
        ("INNERGRID", (0,0), (-1,-1), 0.4, BORDER),
    ]))
    story.append(ct)
    story.append(SP(1, 1.5*cm))
    story.append(P("AI/ML  ·  Weather Intelligence  ·  Flood Risk Analytics  ·  Early Warning Systems", footer_s))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("Table of Contents", h1))
    story.append(section_rule())
    toc_items = [
        ("1.", "Project Overview & Objectives"),
        ("2.", "Dataset Description"),
        ("3.", "Exploratory Data Analysis"),
        ("4.", "Data Preprocessing Pipeline"),
        ("5.", "Feature Engineering"),
        ("6.", "Machine Learning Pipeline"),
        ("7.", "Model Evaluation & Results"),
        ("8.", "Feature Importance & Explainability"),
        ("9.", "System Architecture"),
        ("10.", "Streamlit Application"),
        ("11.", "Key Findings & Insights"),
        ("12.", "Limitations & Future Work"),
        ("13.", "Technologies Used"),
    ]
    for num, title in toc_items:
        story.append(P(f"<b>{num}</b>&nbsp;&nbsp;&nbsp;{title}", toc_s))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # 1. OVERVIEW
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("1. Project Overview &amp; Objectives", h1))
    story.append(section_rule())
    story.append(P(
        "The <b>Nepal Flood Risk Prediction &amp; Early Warning System</b> is an end-to-end "
        "Machine Learning application that analyses daily weather and hydrological observations "
        "from Nepal's major river monitoring stations to predict flood risk levels. The system "
        "is designed as a <b>National Flood Intelligence Center</b>, combining data analytics, "
        "predictive modelling, and a professional interactive web dashboard.", body))

    story.append(P("Objectives", h2))
    for b in [
        "Predict flood risk level (LOW / MEDIUM / HIGH) from observable weather and environmental parameters",
        "Identify the most critical variables driving flood risk across Nepal's river basins",
        "Deliver an accessible, professional early-warning interface for monitoring stations",
        "Demonstrate a complete, reproducible ML pipeline from raw data to deployed prediction",
    ]:
        story.append(P(f"• {b}", bullet))

    story.append(SP(1, 0.3*cm))
    story.append(info_box(
        "<b>Problem Type:</b> Multi-class classification (3 classes: LOW, MEDIUM, HIGH risk)<br/>"
        "<b>Approach:</b> Supervised learning with engineered features and SMOTE-balanced training<br/>"
        "<b>Evaluation Strategy:</b> Time-aware train/test split to simulate real-world forecasting"
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # 2. DATASET
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("2. Dataset Description", h1))
    story.append(section_rule())
    story.append(P(
        "The dataset is sourced from Kaggle: <i>Nepal Flood &amp; Weather Dataset 2023–2026</i> "
        "by Tejal Kunjir. It contains daily hydrological and meteorological records from 10 "
        "monitoring stations across 9 major river basins in Nepal, covering January 2023 to "
        "August 2026.", body))

    # Quick stats
    qs_data = [
        ["Total Records", "Date Range", "Stations", "Rivers", "Missing Values", "Duplicates"],
        ["13,390", "Jan 2023 – Aug 2026", "10", "9", "0", "0"],
    ]
    story.append(table(qs_data, [(W-2*MARGIN)/6]*6))
    story.append(SP(1, 0.25*cm))

    story.append(P("Raw Feature List", h2))
    feat_data = [
        ["Feature", "Type", "Description"],
        ["date", "DateTime", "Observation date (daily)"],
        ["location", "Categorical", "Monitoring station name (10 unique)"],
        ["river", "Categorical", "River name (9 unique)"],
        ["basin", "Categorical", "River basin (9 unique)"],
        ["latitude / longitude", "Float", "Station geographic coordinates"],
        ["elevation_m", "Integer", "Station elevation in metres"],
        ["precipitation_mm", "Float", "Daily total precipitation"],
        ["rain_mm", "Float", "Daily rainfall accumulation"],
        ["soil_moisture_0_100cm_m3m3", "Float", "Volumetric soil moisture (0–100 cm)"],
        ["temperature_mean_c", "Float", "Daily mean temperature"],
        ["dew_point_mean_c", "Float", "Daily mean dew point temperature"],
        ["precipitation_hours", "Integer", "Hours with measurable precipitation"],
        ["relative_humidity_mean_pct", "Integer", "Daily mean relative humidity (%)"],
        ["wind_speed_max_kmh", "Float", "Maximum daily wind speed"],
        ["wind_gusts_max_kmh", "Float", "Maximum daily wind gusts"],
        ["wind_direction_dominant_deg", "Integer", "Dominant wind direction (degrees)"],
        ["river_discharge_m3s", "Float", "River discharge (m³/s) — used to derive target"],
    ]
    cw = [(W-2*MARGIN)*x for x in [0.32, 0.16, 0.52]]
    story.append(table(feat_data, cw))

    story.append(P("Monitoring Stations &amp; Discharge Thresholds", h2))
    thresh_data = [
        ["Station", "River", "p75 (m³/s)", "p90 (m³/s)"],
        ["Kusum",                "West Rapti",  "176.22", "415.87"],
        ["Belsot",               "Kamala",       "43.82",  "91.77"],
        ["Chameliya/Nayalbadi",  "Chamelia",     "43.06",  "87.39"],
        ["Bahrabise",            "Bhote Koshi",   "9.52",  "14.01"],
        ["Devghat",              "Narayani",       "3.56",   "6.04"],
        ["Chatara",              "Saptakoshi",     "2.53",   "4.33"],
        ["Khokana",              "Bagmati",        "2.31",   "4.94"],
        ["Rasuwagadhi",          "Bhote Koshi",    "2.63",   "3.66"],
        ["Chisapani",            "Karnali",        "1.40",   "2.38"],
        ["Bhada Bridge",         "Babai",          "0.33",   "2.29"],
    ]
    cw2 = [(W-2*MARGIN)*x for x in [0.36, 0.28, 0.18, 0.18]]
    story.append(table(thresh_data, cw2))
    story.append(P(
        "Note: Per-station thresholds are critical. Kusum's p90 is 415.87 m³/s while "
        "Bhada Bridge's is only 2.29 m³/s — a global threshold would be meaningless.", caption_s))

    # ══════════════════════════════════════════════════════════════════════════
    # 3. EDA
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("3. Exploratory Data Analysis", h1))
    story.append(section_rule())

    story.append(P("Target Variable Distribution", h2))
    risk_data = [
        ["Class", "Label", "Condition", "Count", "Share"],
        ["0", "LOW",    "discharge < station p75",         "10,032", "74.9%"],
        ["1", "MEDIUM", "p75 ≤ discharge < p90",           "2,013",  "15.0%"],
        ["2", "HIGH",   "discharge ≥ p90",                 "1,345",  "10.0%"],
    ]
    cw3 = [(W-2*MARGIN)*x for x in [0.06, 0.12, 0.46, 0.18, 0.18]]
    story.append(table(risk_data, cw3, extra=[
        ("TEXTCOLOR", (1,1), (1,1), C_LOW),
        ("TEXTCOLOR", (1,2), (1,2), C_MED),
        ("TEXTCOLOR", (1,3), (1,3), C_HIGH),
        ("FONTNAME",  (1,1), (1,3), "Helvetica-Bold"),
    ]))
    story.append(warn_box(
        "The dataset is imbalanced (75% LOW, 15% MEDIUM, 10% HIGH). "
        "SMOTE oversampling was applied to the training set to address this."
    ))

    story.append(P("Precipitation Analysis", h2))
    prec_data = [
        ["Statistic", "Value"],
        ["Daily Mean Precipitation", "4.20 mm"],
        ["Maximum Single-Day Precipitation", "45.61 mm"],
        ["Standard Deviation", "8.45 mm"],
        ["Heavy Rain Days (> 20 mm)", "827 days (6.2%)"],
        ["Peak Month (July)", "12.55 mm/day average"],
        ["Driest Month (December)", "0.09 mm/day average"],
    ]
    story.append(table(prec_data, [(W-2*MARGIN)*0.6, (W-2*MARGIN)*0.4]))

    story.append(P("River Discharge Analysis", h2))
    dis_data = [
        ["Period", "Mean Discharge (m³/s)"],
        ["Overall (all stations)", "20.37"],
        ["Monsoon season (Jun–Sep)", "46.23"],
        ["Winter (Dec–Feb)", "4.34"],
        ["Maximum recorded", "3,175.87  (Kusum station)"],
    ]
    story.append(table(dis_data, [(W-2*MARGIN)*0.6, (W-2*MARGIN)*0.4]))

    story.append(P("Seasonal HIGH-Risk Concentration", h2))
    seas_data = [
        ["Season", "HIGH Risk Events", "Share of All HIGH Events"],
        ["Monsoon (Jun–Sep)",      "1,255", "93.3%"],
        ["Post-Monsoon (Oct–Nov)", "88",    "6.5%"],
        ["Pre-Monsoon (Mar–May)",  "2",     "0.1%"],
        ["Winter (Dec–Feb)",       "0",     "0.0%"],
    ]
    cw4 = [(W-2*MARGIN)*x for x in [0.42, 0.28, 0.30]]
    story.append(table(seas_data, cw4))

    story.append(P("Feature–Risk Correlations (absolute Pearson r)", h2))
    corr_data = [
        ["Feature", "Correlation with Flood Risk", "r Value"],
        ["Dew Point (°C)",           "━━━━━━━━━━━━━━━━━━━", "0.545"],
        ["Relative Humidity (%)",    "━━━━━━━━━━━━━━━━━",   "0.486"],
        ["Soil Moisture",            "━━━━━━━━━━━━━━━━",     "0.457"],
        ["Rainfall (mm)",            "━━━━━━━━━━━━━━",       "0.401"],
        ["Precipitation (mm)",       "━━━━━━━━━━━━━",        "0.397"],
        ["Temperature (°C)",         "━━━━━━━━━━━━",         "0.382"],
        ["River Discharge (m³/s)",   "━━━━━━━━━━",           "0.331"],
        ["Wind Speed (km/h)",        "━━━━━",                "0.150"],
    ]
    cw5 = [(W-2*MARGIN)*x for x in [0.36, 0.46, 0.18]]
    story.append(table(corr_data, cw5))

    # ══════════════════════════════════════════════════════════════════════════
    # 4. PREPROCESSING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("4. Data Preprocessing Pipeline", h1))
    story.append(section_rule())
    story.append(P(
        "The preprocessing pipeline is implemented in <b>src/data_preprocessing.py</b> "
        "and executes the following reproducible steps:", body))
    for step in [
        "<b>1. Duplicate removal</b> — no duplicates found; step retained for robustness",
        "<b>2. Date parsing</b> — date column parsed to datetime64 format",
        "<b>3. Sorting</b> — records sorted by location + date for time-series consistency",
        "<b>4. Date feature extraction</b> — year, month, day_of_year, ISO week",
        "<b>5. Cyclical month encoding</b> — month_sin and month_cos to capture seasonality without ordinal artifacts",
        "<b>6. Missing value imputation</b> — median fill per column (no missing values present; kept for robustness)",
        "<b>7. Outlier capping</b> — 1st–99th percentile winsorisation on precipitation, rainfall, and wind features to preserve real flood extremes",
        "<b>8. Target variable derivation</b> — per-station discharge percentile thresholds (p75 = MEDIUM boundary, p90 = HIGH boundary)",
    ]:
        story.append(P(f"• {step}", bullet))

    story.append(SP(1, 0.2*cm))
    story.append(warn_box(
        "<b>Data Leakage Prevention:</b> Flood risk thresholds (p75, p90) are computed on the "
        "full dataset and saved to disk. In a production setting these would be computed only "
        "on training folds. River discharge is excluded from the model feature set as it is "
        "the source of the target label."
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # 5. FEATURE ENGINEERING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("5. Feature Engineering", h1))
    story.append(section_rule())
    story.append(P(
        "Implemented in <b>src/feature_engineering.py</b>. Starting from 14 base features, "
        "the pipeline engineers 17 additional features for a total of <b>31 model features</b>.", body))

    story.append(P("Rolling Window Features", h2))
    roll_data = [
        ["Window", "Variables", "Aggregations", "Features Added"],
        ["3-day", "precipitation, rain, humidity", "mean, sum", "6"],
        ["7-day", "precipitation, rain, humidity", "mean, sum", "6"],
        ["7-day", "precipitation only",            "max",       "1"],
    ]
    cw6 = [(W-2*MARGIN)*x for x in [0.14, 0.42, 0.28, 0.16]]
    story.append(table(roll_data, cw6))
    story.append(warn_box(
        "<b>Leakage prevention:</b> All rolling features use shift(1) before rolling, "
        "ensuring only past values (not the current day) are used."
    ))

    story.append(P("Domain-Engineered Features", h2))
    eng_data = [
        ["Feature", "Formula", "Rationale"],
        ["saturation_index",  "soil_moisture × (humidity / 100)", "Catchment saturation proxy"],
        ["heavy_rain_flag",   "1 if precipitation > 20 mm",        "Binary heavy-rain event signal"],
        ["temp_dew_spread",   "temperature − dew_point",            "Low spread = near-saturated atmosphere"],
        ["month_sin / cos",   "sin / cos of 2π×month/12",           "Cyclical seasonal encoding"],
        ["location_enc",      "LabelEncoder",                        "Station identity for cross-station differentiation"],
    ]
    cw7 = [(W-2*MARGIN)*x for x in [0.24, 0.36, 0.40]]
    story.append(table(eng_data, cw7))

    # ══════════════════════════════════════════════════════════════════════════
    # 6. ML PIPELINE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("6. Machine Learning Pipeline", h1))
    story.append(section_rule())

    story.append(P("Train / Test Split", h2))
    split_data = [
        ["Split", "Records", "Date Range (approx.)"],
        ["Training set", "10,712  (80%)", "Jan 2023 – mid 2025"],
        ["Test set",     "2,678   (20%)", "mid 2025 – Aug 2026"],
    ]
    story.append(table(split_data, [(W-2*MARGIN)*x for x in [0.24, 0.24, 0.52]]))
    story.append(P(
        "A <b>time-aware split</b> is used: the last 20% of chronologically sorted records form "
        "the test set. This simulates real-world forecasting where the model must generalise to "
        "future, unseen dates — not random held-out samples.", body))

    story.append(P("Class Imbalance — SMOTE", h2))
    story.append(P(
        "SMOTE (Synthetic Minority Oversampling Technique) is applied <b>only to the training "
        "set</b>. It generates synthetic samples for MEDIUM and HIGH classes to achieve a "
        "balanced class distribution of 7,830 samples per class after resampling. "
        "The test set is kept unmodified to reflect real-world class proportions.", body))

    story.append(P("Models Evaluated", h2))
    model_data = [
        ["Model", "Key Hyperparameters"],
        ["Logistic Regression",  "max_iter=1000, class_weight=balanced"],
        ["Decision Tree",        "max_depth=10, class_weight=balanced"],
        ["Random Forest",        "n_estimators=200, max_depth=15, class_weight=balanced, n_jobs=-1"],
        ["Gradient Boosting",    "n_estimators=200, max_depth=5, learning_rate=0.1"],
    ]
    story.append(table(model_data, [(W-2*MARGIN)*0.32, (W-2*MARGIN)*0.68]))

    # ══════════════════════════════════════════════════════════════════════════
    # 7. EVALUATION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("7. Model Evaluation &amp; Results", h1))
    story.append(section_rule())

    perf_data = [
        ["Model", "Accuracy", "Precision", "Recall", "F1 (weighted)", "ROC-AUC"],
        ["Logistic Regression",  "83.83%", "88.93%", "83.83%", "85.55%", "0.9613"],
        ["Decision Tree",        "84.13%", "88.14%", "84.13%", "85.77%", "0.9542"],
        ["Random Forest ★",      "86.71%", "89.17%", "86.71%", "87.65%", "0.9788"],
        ["Gradient Boosting",    "86.22%", "88.91%", "86.22%", "87.26%", "0.9751"],
    ]
    cw8 = [(W-2*MARGIN)*x for x in [0.28, 0.14, 0.14, 0.12, 0.17, 0.15]]
    story.append(table(perf_data, cw8, extra=[
        ("BACKGROUND", (0,3), (-1,3), BLUE_LIGHT),
        ("FONTNAME",   (0,3), (-1,3), "Helvetica-Bold"),
        ("TEXTCOLOR",  (0,3), (-1,3), BLUE),
    ]))
    story.append(P(
        "★ <b>Selected model: Random Forest</b> — highest weighted F1-score (87.65%) and "
        "ROC-AUC (0.9788). Weighted F1 is the primary metric because the test set is imbalanced.", body))

    story.append(P("Classification Report — Random Forest (Test Set)", h2))
    cr_data = [
        ["Class", "Precision", "Recall", "F1-Score", "Support"],
        ["LOW",          "0.99", "0.94", "0.97", "2,202"],
        ["MEDIUM",       "0.47", "0.44", "0.46",   "294"],
        ["HIGH",         "0.38", "0.64", "0.48",   "182"],
        ["Weighted Avg", "0.89", "0.87", "0.88", "2,678"],
    ]
    cw9 = [(W-2*MARGIN)*x for x in [0.28, 0.18, 0.18, 0.18, 0.18]]
    story.append(table(cr_data, cw9, extra=[
        ("TEXTCOLOR",  (0,1),(0,1), C_LOW),
        ("TEXTCOLOR",  (0,2),(0,2), C_MED),
        ("TEXTCOLOR",  (0,3),(0,3), C_HIGH),
        ("FONTNAME",   (0,4),(-1,4), "Helvetica-Bold"),
        ("BACKGROUND", (0,4),(-1,4), BG_CARD),
    ]))
    story.append(info_box(
        "LOW class is predicted with very high accuracy (F1=0.97). MEDIUM and HIGH classes are "
        "harder to classify due to their smaller representation and overlapping feature "
        "distributions. HIGH recall of 0.64 indicates the model successfully flags most genuine "
        "flood-risk events, which is operationally the most important outcome."
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # 8. FEATURE IMPORTANCE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("8. Feature Importance &amp; Explainability", h1))
    story.append(section_rule())
    story.append(P(
        "Random Forest feature importances are computed via mean decrease in Gini impurity "
        "across all 200 trees. The top 15 features are shown below (out of 31 total):", body))

    fi_rows = [
        ("Month (sin)",          "11.47%", 1.00),
        ("Day of Year",          "9.70%",  0.846),
        ("Dew Point (°C)",       "8.31%",  0.724),
        ("Humidity 7-day Avg",   "5.86%",  0.511),
        ("Humidity 7-day Sum",   "5.54%",  0.483),
        ("Rain 7-day Total",     "4.31%",  0.375),
        ("Rain 7-day Avg",       "4.18%",  0.364),
        ("Temperature (°C)",     "3.84%",  0.334),
        ("Soil Moisture",        "3.76%",  0.328),
        ("Humidity 3-day Sum",   "3.74%",  0.326),
        ("Month (cos)",          "3.68%",  0.320),
        ("Precip 7-day Total",   "3.44%",  0.300),
        ("Saturation Index",     "3.33%",  0.290),
        ("Humidity 3-day Avg",   "3.25%",  0.283),
        ("Precip 7-day Avg",     "3.09%",  0.269),
    ]
    story.append(bar_table(fi_rows))

    story.append(SP(1, 0.2*cm))
    story.append(info_box(
        "<b>Key insight:</b> Seasonality features (month_sin, day_of_year) dominate because "
        "flood risk in Nepal is overwhelmingly monsoon-driven (93.3% of HIGH events in Jun–Sep). "
        "After seasonality, dew point, rolling humidity windows, and rolling rainfall are the "
        "strongest predictors — reflecting cumulative moisture build-up that precedes flooding.<br/><br/>"
        "Feature importance reflects how strongly variables contribute to model predictions across "
        "the training dataset. It does not establish direct causation."
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # 9. ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("9. System Architecture", h1))
    story.append(section_rule())

    arch_data = [
        ["Component", "File", "Responsibility"],
        ["Data Ingestion",     "data/CORRECTED_...csv",        "Raw daily weather & hydrological records"],
        ["Preprocessing",      "src/data_preprocessing.py",   "Cleaning, label derivation, date features"],
        ["Feature Engineering","src/feature_engineering.py",  "Rolling windows, encoding, domain features"],
        ["Model Training",     "src/train_model.py",           "SMOTE, fit 4 classifiers, evaluate, save"],
        ["Inference",          "src/predict.py",               "Live prediction from user input"],
        ["Utilities",          "src/utils.py",                 "Shared helpers, metrics loading, formatting"],
        ["Model Artifacts",    "models/",                      "*.pkl, thresholds.csv, metrics.json, plots"],
        ["Dashboard",          "app.py",                       "Streamlit 7-page professional dashboard"],
        ["Notebook",           "notebooks/EDA_and_Modeling.ipynb", "53-cell EDA and modelling walkthrough"],
    ]
    cw10 = [(W-2*MARGIN)*x for x in [0.22, 0.32, 0.46]]
    story.append(table(arch_data, cw10))

    # ══════════════════════════════════════════════════════════════════════════
    # 10. STREAMLIT APP
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("10. Streamlit Application", h1))
    story.append(section_rule())
    story.append(P(
        "The application is built as a <b>National Flood Intelligence Center</b> with a "
        "professional dark-navy sidebar navigation and 7 functional pages:", body))

    pages_data = [
        ["Page", "Description"],
        ["Dashboard",            "Command center: KPI cards, live risk status, donut chart, seasonal pattern, precipitation trend, station network table, key insights"],
        ["Flood Risk Prediction","Grouped input form (weather / environmental conditions), real-time model inference, prediction card with confidence, probability bars, feature importance"],
        ["Data Analysis",        "4-tab interactive workspace: Weather Analysis, Hydrological Analysis, Risk Analysis, Correlations — with station/year/risk level filters"],
        ["Model Performance",    "Metric cards, model comparison chart (F1 + AUC), confusion matrix, feature importance chart, model summary row, methodology expander"],
        ["Station Monitoring",   "Per-station deep-dive: KPIs, discharge timeline, precipitation timeline, monthly risk breakdown"],
        ["Risk Trends",          "Early Warning Center: alert cards per station, 30-day rolling risk trend lines, scrollable risk event timeline"],
        ["Regional Insights",    "Basin-level risk profiles, elevation vs risk scatter, season × basin heatmap"],
    ]
    cw11 = [(W-2*MARGIN)*0.28, (W-2*MARGIN)*0.72]
    story.append(table(pages_data, cw11))

    # ══════════════════════════════════════════════════════════════════════════
    # 11. KEY FINDINGS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("11. Key Findings &amp; Insights", h1))
    story.append(section_rule())

    findings = [
        ("Extreme Seasonal Concentration",
         "93.3% of all HIGH-risk events occur during the monsoon season (June–September). "
         "Risk is negligible in winter, confirming the dominant role of the South Asian monsoon "
         "in Nepal's flood cycle."),
        ("Peak Risk Month: July",
         "July records the highest average daily precipitation (12.55 mm) and the highest "
         "frequency of HIGH and MEDIUM risk events. Monthly discharge is 10× higher in "
         "July–August compared to winter months."),
        ("Cumulative Moisture Matters Most",
         "Rolling 7-day humidity and rainfall windows rank among the top 5 features. This "
         "confirms that antecedent soil saturation and atmospheric moisture are stronger "
         "predictors than single-day precipitation alone."),
        ("Dew Point as a Flood Predictor",
         "Dew point has the highest single-feature correlation with flood risk (r=0.545). "
         "A high dew point indicates a saturated, moisture-laden atmosphere — conditions "
         "that reliably precede heavy rainfall and elevated discharge."),
        ("Per-Station Thresholds Are Essential",
         "Kusum's p90 threshold is 415.87 m³/s while Bhada Bridge's is only 2.29 m³/s. "
         "A global threshold would misclassify nearly all records at smaller stations, making "
         "per-station normalisation a critical design decision."),
        ("Random Forest Outperforms All Baselines",
         "Random Forest achieves 87.65% weighted F1 and 0.9788 ROC-AUC — outperforming "
         "Gradient Boosting (87.26%), Decision Tree (85.77%), and Logistic Regression (85.55%). "
         "Its ensemble structure handles the non-linear, strongly seasonal patterns effectively."),
    ]
    for title, body_text in findings:
        story.append(P(f"<b>{title}</b>", h2))
        story.append(P(body_text, body))

    # ══════════════════════════════════════════════════════════════════════════
    # 12. LIMITATIONS & FUTURE WORK
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("12. Limitations &amp; Future Work", h1))
    story.append(section_rule())

    story.append(P("Current Limitations", h2))
    for lim in [
        "<b>No real-time data feed</b> — predictions require manually entered parameters; no live API integration",
        "<b>MEDIUM/HIGH class performance</b> — F1 scores of 0.46–0.48 for minority classes; additional training data would help",
        "<b>No spatial modelling</b> — geographic proximity between stations is not exploited; upstream conditions do not inform downstream predictions",
        "<b>Static thresholds</b> — p75/p90 thresholds computed on the full dataset; production implementation should use training-only data per cross-validation fold",
        "<b>No snowmelt features</b> — for high-elevation stations (e.g., Rasuwagadhi at 1,749 m), snowmelt is a significant flood driver not captured in the current feature set",
    ]:
        story.append(P(f"• {lim}", bullet))

    story.append(P("Future Improvements", h2))
    for fut in [
        "Integrate OpenWeatherMap or DHM Nepal real-time API for live data ingestion",
        "Implement XGBoost / LightGBM with Bayesian hyperparameter optimisation",
        "Add LSTM or Temporal Fusion Transformer for sequence-aware multi-step forecasting",
        "Build upstream-to-downstream station routing to capture catchment-level signals",
        "Add SHAP values for per-prediction explainability beyond global feature importance",
        "Deploy on Streamlit Community Cloud or AWS EC2 for public access",
    ]:
        story.append(P(f"• {fut}", bullet))

    # ══════════════════════════════════════════════════════════════════════════
    # 13. TECH STACK
    # ══════════════════════════════════════════════════════════════════════════
    story.append(P("13. Technologies Used", h1))
    story.append(section_rule())

    tech_data = [
        ["Category", "Technology", "Purpose"],
        ["Language",       "Python 3.10+",            "Complete backend and frontend"],
        ["Data",           "pandas, numpy",            "Data manipulation and numerical computation"],
        ["ML Framework",   "scikit-learn 1.4+",        "Model training, evaluation, preprocessing"],
        ["Imbalance",      "imbalanced-learn",         "SMOTE oversampling"],
        ["Visualisation",  "Plotly, matplotlib, seaborn", "Interactive charts and saved EDA plots"],
        ["Frontend",       "Streamlit 1.35+",          "7-page web dashboard"],
        ["Persistence",    "joblib",                   "Model and encoder serialisation"],
        ["Notebooks",      "Jupyter / nbformat",       "53-cell EDA and modelling notebook"],
        ["Dataset Source", "Kaggle",                   "Nepal Flood & Weather Dataset 2023–2026"],
    ]
    cw12 = [(W-2*MARGIN)*x for x in [0.22, 0.30, 0.48]]
    story.append(table(tech_data, cw12))

    # ══════════════════════════════════════════════════════════════════════════
    # FINAL NOTE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(SP(1, 0.8*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    story.append(SP(1, 0.3*cm))
    story.append(P(
        "<b>Nepal Flood Risk Prediction &amp; Early Warning System</b><br/>"
        "All metrics, statistics, and model results in this report are derived from the actual "
        "trained Random Forest classifier and the Nepal Flood &amp; Weather Dataset 2023–2026.<br/>"
        "AI/ML  ·  Weather Intelligence  ·  Flood Risk Analytics  ·  Python · scikit-learn · Streamlit",
        footer_s))

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)
    print(f"PDF saved: {out}")
    return out

if __name__ == "__main__":
    build()
