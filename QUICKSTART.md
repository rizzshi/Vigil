# 🚀 Algorzen Vigil - Quick Start Guide
**Algorzen Research Division © 2025 — Author Rishi Singh**

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis (CLI)
```bash
python main.py --input data/sample_kpi_data.csv
```

### 3. Launch Web Interface
```bash
streamlit run app/streamlit_app.py
```

---

## 📊 What You Get

✅ **Console Output**: Real-time analysis progress  
✅ **PDF Report**: `reports/Vigil_Report_YYYY-MM-DD.pdf`  
✅ **Metadata JSON**: `reports/report_metadata.json`  
✅ **Visualizations**: Time-series charts with anomaly highlights  

---

## 🤖 Enable AI Analysis (Optional)

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```

2. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. Run with AI flag:
   ```bash
   python main.py --input data/sample_kpi_data.csv --use-openai
   ```

---

## 🎯 Common Commands

**Basic analysis:**
```bash
python main.py --input data/sample_kpi_data.csv
```

**Custom thresholds:**
```bash
python main.py --input data/sample_kpi_data.csv --zscore-threshold 2.5 --rolling-window 14
```

**Full AI-powered analysis:**
```bash
python main.py --input data/sample_kpi_data.csv --use-openai
```

**Help:**
```bash
python main.py --help
```

---

## 📁 Your Data Format

Ensure your CSV has:
- A date column (any name, specify with `--date-column`)
- One or more numeric KPI columns

**Example:**
```csv
date,revenue,users,churn_rate
2024-01-01,100000,500,2.1
2024-01-02,105000,520,2.0
```

---

## 🆘 Troubleshooting

**Import errors?**
```bash
pip install -r requirements.txt
```

**OpenAI errors?**
- Don't use `--use-openai` without API key
- System works fine without it (fallback mode)

**Can't find date column?**
```bash
python main.py --input yourfile.csv --date-column timestamp
```

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Algorzen Research Division — Powering Data Intelligence**
