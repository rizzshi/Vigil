# 🧠 Algorzen Vigil

**AI Drift Detection & Anomaly Monitoring Engine**

*Algorzen Research Division © 2025 — Author Rishi Singh*  
*Project Drop 002*

---

## 🎯 Overview

Algorzen Vigil is an enterprise-grade AI-powered drift detection and anomaly monitoring system designed for time-series KPI analysis. Built with executive business insights in mind, Vigil combines advanced statistical methods with optional GPT-4 integration to deliver actionable intelligence through professional PDF reports.

### Key Features

- **🎯 Multi-Method Anomaly Detection**
  - Z-score outlier detection (configurable σ threshold)
  - Rolling median deviation analysis (>25% default)
  - Seasonal trend decomposition
  
- **🤖 AI-Powered Narrative Engine**
  - GPT-4 integration for executive summaries
  - Intelligent root cause analysis
  - Actionable recommendations
  - Fallback heuristic explanations
  
- **📄 Professional PDF Reports**
  - Algorzen Research Division branding
  - Time-series visualizations with anomaly highlights
  - Executive narrative sections
  - KPI statistics tables
  - Metadata JSON export
  
- **🌐 Interactive Web Interface**
  - Streamlit-powered UI
  - File upload and analysis
  - Real-time visualization
  - One-click PDF generation

---

## 🏗️ Architecture

```
algorzen-vigil/
├── main.py                    # CLI entry point
├── drift_detector.py          # Anomaly detection algorithms
├── anomaly_explainer.py       # AI narrative generation
├── report_generator.py        # PDF report builder
├── app/
│   └── streamlit_app.py      # Web interface
├── data/
│   └── sample_kpi_data.csv   # Sample dataset
├── reports/                   # Generated reports
│   ├── Vigil_Report_*.pdf
│   └── report_metadata.json
├── requirements.txt           # Python dependencies
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/algorzen/vigil.git
   cd vigil
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API (optional)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

---

## 🚀 Usage

### Command-Line Interface

**Basic usage:**
```bash
python main.py --input data/sample_kpi_data.csv
```

**With OpenAI GPT-4:**
```bash
python main.py --input data/sample_kpi_data.csv --use-openai
```

**Custom parameters:**
```bash
python main.py \
  --input data/sample_kpi_data.csv \
  --zscore-threshold 2.5 \
  --rolling-window 14 \
  --deviation-threshold 0.30 \
  --output-dir custom_reports \
  --use-openai
```

**CLI Options:**
- `--input, -i`: Path to input CSV file (required)
- `--output-dir, -o`: Output directory for reports (default: `reports`)
- `--use-openai`: Enable GPT-4 explanations
- `--zscore-threshold`: Z-score threshold (default: 3.0)
- `--rolling-window`: Rolling window size in days (default: 7)
- `--deviation-threshold`: Deviation threshold percentage (default: 0.25)
- `--date-column`: Name of date column (default: `date`)
- `--report-id`: Custom report identifier

### Web Interface

**Launch Streamlit app:**
```bash
streamlit run app/streamlit_app.py
```

Then navigate to `http://localhost:8501` in your browser.

**Web features:**
- Upload CSV files
- Configure detection parameters
- Interactive visualizations
- Real-time analysis
- Download PDF reports

---

## 📊 Input Data Format

Your CSV file should contain:
- A date/timestamp column (configurable name)
- One or more numeric KPI columns

**Example:**
```csv
date,revenue,customer_acquisition,churn_rate,server_uptime,api_latency
2024-01-01,125000,450,2.1,99.95,120
2024-01-02,128000,465,2.0,99.97,115
2024-01-03,130000,472,1.9,99.96,118
```

---

## 📈 Example Output

### Console Output
```
==============================================================================
🧠 Algorzen Vigil - AI Drift Detection Engine
Algorzen Research Division © 2025 — Author Rishi Singh
Project Drop 002 — Anomaly Monitoring & Analytics
==============================================================================

📂 Loading KPI data from: data/sample_kpi_data.csv
✅ Loaded 90 records with 6 columns

🔍 Initializing drift detection system...
✅ Monitoring 5 KPIs: revenue, customer_acquisition, churn_rate, server_uptime, api_latency

🎯 Running Z-score outlier detection (threshold: 3.0σ)...
✅ Found 3 Z-score outliers

📊 Total Anomalies: 8
⚠️  Severity Level: Medium
📈 KPIs Analyzed: 5
📄 Report Location: reports/Vigil_Report_2025-11-10.pdf
```

### PDF Report Contents
- **Executive Summary**: AI-generated business insights
- **Anomaly Overview**: Total count, severity, affected KPIs
- **Key Findings**: Detailed analysis of detected anomalies
- **Recommendations**: Actionable next steps
- **KPI Statistics**: Mean, std dev, min, max for each metric
- **Visualizations**: Time-series charts with anomaly highlights

### Metadata JSON
```json
{
  "project": "Algorzen Vigil",
  "report_id": "VIGIL-2025-Q4-001",
  "generated_by": "Rishi Singh",
  "created_at": "2025-11-10T14:30:00",
  "tone": "Executive Business",
  "openai_used": true,
  "anomaly_summary": {
    "total_anomalies": 8,
    "severity": "Medium",
    "affected_kpis": ["revenue", "churn_rate", "server_uptime"]
  }
}
```

---

## 🧩 Module Overview

### `drift_detector.py`
Core anomaly detection algorithms:
- **Z-score Analysis**: Identifies extreme outliers beyond configurable standard deviations
- **Rolling Deviation**: Detects rapid changes from recent trends
- **Seasonal Decomposition**: Separates trend, seasonal, and residual components
- **Statistical Summaries**: Comprehensive KPI statistics

### `anomaly_explainer.py`
AI-powered narrative generation:
- **GPT-4 Integration**: Intelligent analysis using OpenAI API
- **Fallback Engine**: Heuristic-based explanations when API unavailable
- **Executive Tone**: Business-focused, concise, actionable insights
- **Multi-Section Output**: Summary, findings, recommendations

### `report_generator.py`
Professional PDF creation:
- **Algorzen Branding**: Custom headers, footers, styling
- **Chart Generation**: Matplotlib/Seaborn visualizations
- **Table Formatting**: ReportLab tables for statistics
- **Metadata Export**: JSON file with report metadata

### `main.py`
Command-line orchestration:
- **Argument Parsing**: Flexible CLI configuration
- **Pipeline Execution**: Coordinated analysis workflow
- **Progress Feedback**: Real-time status updates
- **Error Handling**: Graceful failure recovery

### `app/streamlit_app.py`
Interactive web interface:
- **File Upload**: CSV drag-and-drop
- **Parameter Controls**: Sliders and inputs
- **Live Visualization**: Interactive charts
- **Report Download**: One-click PDF generation

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI API Configuration (optional)
OPENAI_API_KEY=sk-your-api-key-here
```

### Detection Parameters

All detection thresholds are configurable:

- **Z-Score Threshold**: 1.0 - 5.0 (default: 3.0)
  - Lower = more sensitive, more anomalies
  - Higher = less sensitive, fewer anomalies

- **Rolling Window**: 3 - 30 days (default: 7)
  - Smaller = detects short-term changes
  - Larger = detects long-term trends

- **Deviation Threshold**: 10% - 50% (default: 25%)
  - Lower = more sensitive to deviations
  - Higher = only major deviations flagged

---

## 💼 Business Value

### For Executives
- **Executive Summaries**: AI-generated insights in business language
- **Risk Assessment**: Severity-based anomaly classification
- **Actionable Recommendations**: Clear next steps for intervention

### For Data Teams
- **Multi-Method Detection**: Comprehensive anomaly coverage
- **Configurable Thresholds**: Tune sensitivity to your needs
- **Automated Reporting**: Consistent, reproducible analysis

### For Operations
- **Early Warning System**: Detect issues before they escalate
- **Root Cause Analysis**: AI-powered explanations
- **Audit Trail**: Metadata tracking for compliance

---

## 🧪 Running Tests

Test with the included sample data:

```bash
python main.py --input data/sample_kpi_data.csv
```

Expected output:
- Console log showing analysis progress
- PDF report in `reports/` directory
- Metadata JSON file
- Multiple visualization PNG files

---

## 🛠️ Troubleshooting

### ImportError: No module named 'openai'
```bash
pip install -r requirements.txt
```

### OpenAI API errors
- Verify `OPENAI_API_KEY` in `.env`
- Use `--use-openai` flag only if API key is set
- Fallback mode works without API key

### Date parsing issues
- Ensure CSV has a date column
- Specify column name with `--date-column`
- Date format: YYYY-MM-DD recommended

### Memory issues with large datasets
- Process data in chunks
- Reduce rolling window size
- Limit visualizations to top KPIs

---

## 📚 Dependencies

- **pandas** (≥2.0.0): Data manipulation
- **numpy** (≥1.24.0): Numerical computing
- **scipy** (≥1.10.0): Statistical functions
- **statsmodels** (≥0.14.0): Time-series analysis
- **matplotlib** (≥3.7.0): Visualization
- **seaborn** (≥0.12.0): Statistical plotting
- **reportlab** (≥4.0.0): PDF generation
- **openai** (≥1.0.0): GPT-4 integration
- **streamlit** (≥1.28.0): Web interface
- **python-dotenv** (≥1.0.0): Environment management

---

## 📝 License

Copyright © 2025 Algorzen Research Division

This project is proprietary software developed by Rishi Singh for Algorzen Research Division.

---

## 🧠 About Algorzen Research Division

Algorzen Research Division develops cutting-edge AI and data intelligence solutions for enterprise analytics. We combine academic rigor with business pragmatism to deliver actionable insights at scale.

**Project Drops:**
- Drop 001: [Classified]
- **Drop 002: Vigil (AI Drift Detection Engine)** ← You are here
- Drop 003: [Coming Soon]

---

## 👤 Author

**Rishi Singh**  
Lead Researcher, Algorzen Research Division

For questions, collaborations, or enterprise licensing:
- GitHub: [Your GitHub Profile]
- Email: [Your Email]
- Website: [Algorzen Website]

---

## 🙏 Acknowledgments

Built with:
- Python ecosystem (NumPy, Pandas, SciPy)
- OpenAI GPT-4 API
- ReportLab PDF Library
- Streamlit Framework

---

## �️ Screenshots & Demo

Below are placeholders for screenshots that illustrate the working Vigil app. Add your exported PNGs to `docs/assets/` with the filenames shown below and they will render here.

### 1) App Overview
![Overview](docs/assets/screenshot_overview.png)
*Caption: Landing / dashboard view showing high-level summary.*

### 2) Upload Data
![Upload](docs/assets/screenshot_upload.png)
*Caption: CSV upload and parameter controls.*

### 3) Analysis Results
![Results](docs/assets/screenshot_results.png)
*Caption: Detected anomalies, KPIs, and metrics table.*

### 4) Advanced Analytics
![Advanced](docs/assets/screenshot_advanced.png)
*Caption: Correlation heatmap, seasonal decomposition, distribution analysis.*

### 5) PDF Report Preview
![PDF Report](docs/assets/screenshot_pdf.png)
*Caption: Example of the PDF report generated by the project.*

### Premium Features (Placeholder)
![Premium](docs/assets/screenshot_premium.png)
*Caption: Reserved slot — upgrade to access premium dashboards and extended analytics. This image is a placeholder that can contain a Paywall CTA, screenshot of premium charts, or a lock overlay indicating gated features.*

Notes on images:
- Recommended format: PNG
- Suggested sizes: 1000–1400px width for landscape images
- If screenshots are not present, GitHub will show broken image icons; keep `docs/assets/README.md` for guidance.

## �📅 Version History

- **v1.0.0** (2025-11-10): Initial release
  - Multi-method anomaly detection
  - GPT-4 integration with fallback
  - PDF report generation
  - Streamlit web interface
  - Complete documentation

---

**Algorzen Research Division © 2025 — Author Rishi Singh**  
*Powering Data Intelligence*
