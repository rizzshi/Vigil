# 📦 Installation Guide - Algorzen Vigil
**Algorzen Research Division © 2025 — Author Rishi Singh**

---

## System Requirements

- **Python**: 3.10 or higher
- **Operating System**: macOS, Linux, or Windows
- **Memory**: 2GB RAM minimum
- **Storage**: 100MB free space

---

## Installation Methods

### Method 1: Automated Setup (Recommended)

```bash
# Clone or download the project
cd algorzen-vigil

# Run automated setup
python setup.py
```

This will:
1. ✅ Check Python version
2. ✅ Install all dependencies
3. ✅ Create environment configuration
4. ✅ Run test analysis
5. ✅ Generate sample report

---

### Method 2: Manual Installation

#### Step 1: Create Virtual Environment (Recommended)

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment (Optional)

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

#### Step 4: Test Installation

```bash
python main.py --input data/sample_kpi_data.csv
```

---

## Dependency Installation Issues

### Issue: `pip install` fails

**Solution 1: Upgrade pip**
```bash
python -m pip install --upgrade pip
```

**Solution 2: Install with user flag**
```bash
pip install --user -r requirements.txt
```

**Solution 3: Install individually**
```bash
pip install pandas numpy scipy statsmodels
pip install matplotlib seaborn reportlab
pip install openai streamlit python-dotenv pillow
```

---

### Issue: `ImportError: No module named 'numpy'`

**Solution:**
```bash
pip install numpy
pip install -r requirements.txt
```

---

### Issue: ReportLab installation fails

**macOS:**
```bash
brew install freetype
pip install reportlab
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libfreetype6-dev
pip install reportlab
```

**Windows:**
```bash
# Download pre-built wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#reportlab
pip install reportlab-*.whl
```

---

## Platform-Specific Instructions

### macOS

```bash
# Install Python 3.10+ via Homebrew
brew install python@3.10

# Clone project
cd algorzen-vigil

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run test
python main.py --input data/sample_kpi_data.csv
```

---

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.10+
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Clone project
cd algorzen-vigil

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run test
python main.py --input data/sample_kpi_data.csv
```

---

### Windows

```cmd
# Download Python 3.10+ from python.org

# Clone project
cd algorzen-vigil

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run test
python main.py --input data\sample_kpi_data.csv
```

---

## Verifying Installation

### Check Python Version
```bash
python --version
# Should show: Python 3.10.x or higher
```

### Check Installed Packages
```bash
pip list | grep -E "pandas|numpy|openai|streamlit"
```

### Run Quick Test
```bash
python -c "import pandas, numpy, openai, streamlit; print('✅ All imports successful')"
```

---

## Optional: OpenAI Integration

### Step 1: Get API Key
1. Visit: https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key (starts with `sk-`)

### Step 2: Configure
```bash
# Create .env file
cp .env.example .env

# Edit .env and add:
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 3: Test
```bash
python main.py --input data/sample_kpi_data.csv --use-openai
```

**Note**: System works perfectly without OpenAI using fallback mode.

---

## Running the Applications

### CLI Application
```bash
python main.py --input data/sample_kpi_data.csv
```

### Web Interface
```bash
streamlit run app/streamlit_app.py
# Opens browser at http://localhost:8501
```

---

## Uninstallation

### Remove Virtual Environment
```bash
deactivate  # Exit venv first
rm -rf venv
```

### Remove Dependencies (if installed globally)
```bash
pip uninstall -r requirements.txt -y
```

---

## Upgrading

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package
```bash
pip install --upgrade openai
```

---

## Docker Installation (Advanced)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py", "--input", "data/sample_kpi_data.csv"]
```

Build and run:
```bash
docker build -t algorzen-vigil .
docker run -v $(pwd)/reports:/app/reports algorzen-vigil
```

---

## Getting Help

### Error Logs
Check the console output for detailed error messages.

### Common Issues
- **Import errors**: Run `pip install -r requirements.txt`
- **Permission errors**: Use `pip install --user`
- **OpenAI errors**: Don't use `--use-openai` without API key

### Support
- Check `README.md` for documentation
- Review `QUICKSTART.md` for quick fixes
- See `PROJECT_SUMMARY.md` for overview

---

## Next Steps After Installation

1. ✅ Review sample report in `reports/`
2. ✅ Read `QUICKSTART.md` for usage examples
3. ✅ Explore CLI options: `python main.py --help`
4. ✅ Try web interface: `streamlit run app/streamlit_app.py`
5. ✅ Test with your own data

---

**Algorzen Research Division © 2025 — Author Rishi Singh**  
*Installation complete. Ready to detect anomalies!*
