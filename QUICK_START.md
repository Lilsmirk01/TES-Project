# 🚀 Quick Start Guide

## 30-Second Setup

### 1. Install Dependencies
```bash
python3 -m venv .venv
. .venv/bin/activate  # or: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Run the App
```bash
# Option 1: using the venv run script
./run.sh

# Option 2: directly with the venv Python/Streamlit
.venv/bin/streamlit run app.py
```

**Done!** Your browser opens at `http://localhost:8501`

---

## Test It First (Console)

Before running the web app, verify the system works:

```bash
python inference_engine.py
```

Expected output:
```
Running verification test case (hard-coded patient):
 - COVID-19: 75.9% match
 - Pneumonia: 36.8% match
 - Acute Bronchitis: 31.8% match
 - Asthma: 27.3% match
```

---

## Using the Web Interface

1. **Fill in demographics** (age, gender) in the sidebar
2. **Check symptoms** (fever, cough, etc.) in the main area
3. **Click "Diagnose"** button
4. **Review results** with top 2 diseases and recommendations

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: streamlit` | Run: `pip install -r requirements.txt` |
| Browser doesn't open | Go to: `http://localhost:8501` |
| Port 8501 in use | Run: `streamlit run app.py --server.port 8502` |
| Need help | Read: `help.md` |

---

## Project Files

- **app.py** - Web interface (Streamlit)
- **inference_engine.py** - AI reasoning logic
- **knowledge_base.py** - Medical rules & symptoms
- **help.md** - Complete documentation
- **README.md** - Project overview

---

**Ready to diagnose!** 🏥
