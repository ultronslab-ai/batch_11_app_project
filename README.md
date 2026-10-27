# 🛡️ OIL Safety Intelligence Engine (SIH26165)
> **AI/NLP Engine to Detect Serious Injury & Fatality (SIF) Precursors & IOGP Life-Saving Rule Violations in Oil India Limited (OIL) Safety Reports**

---

## 🎯 Problem Statement Overview
In oil and gas exploration and production operations (OIL), thousands of Unsafe-Act, Unsafe-Condition, and Near-Miss reports are recorded annually across rig sites, compressor stations, pipelines, and refineries.

**The Key Challenge:** Less than 15% of these safety reports contain critical **Serious Injury & Fatality (SIF) Precursors**. Manual review is slow, subjective, and prone to missing subtle high-risk precursor patterns.

**Our Solution:** An end-to-end AI/NLP decision-support web application that ingests unstructured free-text safety reports, quantifies SIF probability, tags relevant **IOGP Life-Saving Rules**, extracts structured precursors (Equipment, Barrier Failures, Unsafe Conditions), and presents actionable HSE risk density rankings.

---

## 🌟 Key Features

1. **📱 Worker Direct Field Reporting Portal & 🎙️ Regional Voice Input:**
   - Field operators & technicians can **speak via microphone** or type in **Assamese (অসমীয়া), Hindi (हिंदी), Bengali (বাংলা), or English**.
   - HTML5 Web Speech API integration transcribes spoken regional audio in real-time.
   - Multilingual NLP normalization engine automatically translates regional safety vocabulary into standardized English HSE incident reports.
   - Displays instant real-time AI confirmation with SIF Risk Badge, 1-10 Risk Score, tagged IOGP Life-Saving Rules, and rationale.

2. **⚡ Live Single Report NLP Inspector:**
   - Free-text input & preset test scenarios.
   - SIF Probability % Gauge & Binary Classification (`SIF-Potential` / `Non-SIF`).
   - Automated Multi-Label Tagging for all 10 **IOGP Life-Saving Rules**.
   - Model Explainability (highlights exact precursor trigger words).

2. **📁 Batch CSV Ingestion & Scoring:**
   - Drag-and-drop CSV upload supporting `report_id`, `report_text`, `site`, `date`, `category`, `activity`.
   - Batch scoring with automated validation and one-click downloadable scored CSV.

3. **📊 Executive HSE Intelligence Dashboard:**
   - High-level KPIs: Total Reports, SIF Count, SIF Density %, Top Violated Life-Saving Rule, Highest Risk Site.
   - Monthly trend comparison (SIF vs. Non-SIF).
   - IOGP Life-Saving Rule distribution & common precursor phrase frequency.

4. **🗺️ Risk Hotspots & Precursor Density Rankings:**
   - Site & Activity ranking by **SIF-Precursor Density %** ($(\text{SIF Reports} / \text{Total Reports}) \times 100$).
   - Interactive Risk Heatmap Matrix (Site vs. Activity SIF probability %).

5. **🔎 Deep Drill-Down Inspection:**
   - Searchable, multi-filterable tabular inspection view with detailed expandable cards.

---

## 📜 Supported IOGP Life-Saving Rules

- ⚡ **Energy Isolation**
- 🔥 **Hot Work**
- 🛢️ **Confined Space**
- 🎯 **Line of Fire**
- 🧗 **Working at Height**
- 🏗️ **Lifting Operations**
- 🚚 **Driving**
- ⛏️ **Excavation**
- 📄 **Permit to Work**
- ⛔ **Bypassing Safety Controls**

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Model Evaluation Script
```bash
python evaluate.py
```
*Outputs validation metrics including Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix.*

### 3. Launch Web Application
```bash
streamlit run app.py
```
*The web app will open automatically at `http://localhost:8501`.*

---

## ⏱️ 2-Minute Judge Walkthrough Guide

1. **Open App:** Go to `http://localhost:8501`.
2. **Tab 1 ("How It Works"):** Review the 10 IOGP Life-Saving Rules and core 3-tier architecture.
3. **Tab 2 ("Single Report Inspector"):** Select a preset scenario like *"Working at Height"* or *"Hot Work & Gas Testing"*, click **Analyze**, and observe the SIF probability gauge, IOGP rule tags, and model explainability text.
4. **Tab 3 ("Batch CSV Processor"):** Click download scored CSV or inspect current dataset.
5. **Tab 4 & 5 ("HSE Analytics" & "Risk Hotspots"):** View executive KPIs, monthly trends, and the Site vs Activity Risk Heatmap.
6. **Tab 6 ("Drill-Down"):** Filter reports by site or keyword to inspect individual incident details.

---

## 📂 Project Architecture

```
sih 2k26/
├── data/
│   └── sample_sif_reports.csv       # Synthetic dataset of 40+ realistic OIL safety reports
├── src/
│   ├── __init__.py                  # Package init
│   ├── ingestion.py                 # Data validation & text normalization
│   ├── sif_classifier.py            # SIF Classifier (TF-IDF + Calibrated Logistic Regression)
│   ├── lsr_tagger.py                # Multi-label tagger for 10 IOGP Life-Saving Rules
│   ├── precursor_extractor.py       # Precursor entity & barrier failure extractor
│   ├── analytics.py                 # Risk density calculations, heatmaps & rankings
│   └── utils.py                     # Custom CSS styles, badge formatters & constants
├── app.py                           # Main Streamlit Web Application
├── evaluate.py                      # Model validation script
├── requirements.txt                 # Dependencies
└── README.md                        # Setup and documentation
```

---

## 🏆 SIH Hackathon Evaluation Alignment

- **SIF Classification:** Yes (TF-IDF + Calibrated Logistic Model + Rule-based triggers).
- **Life-Saving Rules:** Yes (All 10 IOGP rules tagged multi-label).
- **Precursor Patterns:** Extracted (Activity, Location, Equipment, Barrier Failure, Unsafe Condition).
- **Dashboard & Rankings:** SIF Precursor Density ranking by Site & Activity.
- **Explainability:** Feature attribution & rationale provided for every prediction.
