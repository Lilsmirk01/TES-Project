# 🎯 How to Run Your Expert System

This guide shows you exactly how to set up and run the Respiratory Disease Diagnosis Expert System.

---

## 📦 Step 1: Install Dependencies (One-Time Setup)

Open **PowerShell** or **Command Prompt** in your project folder:

```powershell
cd c:\Users\dylan\Documents\GitHub\TES-Project
pip install -r requirements.txt
```

**Expected output:** Streamlit and dependencies install successfully ✅

---

## 🌐 Step 2: Run the Interactive Web App (Recommended)

```powershell
streamlit run app.py
```

**What happens:**
- Your default browser opens automatically
- If not, go to: **http://localhost:8501**
- You see the Respiratory Disease Diagnosis interface
- Enter symptoms and click "Diagnose" to get results

**To stop:** Press `Ctrl+C` in PowerShell

---

## 🧪 Step 3: Run Verification Tests (No UI)

To verify the system works without the web interface:

### Option A: Quick Test
```powershell
python inference_engine.py
```

### Option B: Same Test (Alternative)
```powershell
python verify_run.py
```

**Expected output:**
```
Running verification test case (hard-coded patient):
 - COVID-19: 75.9% match
 - Pneumonia: 36.8% match
 - Acute Bronchitis: 31.8% match
 - Asthma: 27.3% match
```

This proves the system is working correctly. ✅

---

## 📚 Step 4: Inspect the Knowledge Base

See all diseases and symptoms defined in the system:

```powershell
python knowledge_base.py
```

**Expected output:**
```
Defined diseases:
 - Asthma
 - COPD
 - Pneumonia
 - COVID-19
 - Tuberculosis
 - Acute Bronchitis

Symptom keys:
['chest_pain', 'cough_blood', 'cough_dry', 'cough_wet', 'fatigue', 
'fever_high', 'fever_low', 'fever_none', 'loss_taste_smell', 
'shortness_of_breath', 'smoking_history', 'wheezing']
```

---

## 🎨 Using the Web Interface

Once `streamlit run app.py` is running and your browser shows the app:

### In the Sidebar:
1. **Enter Age** (0-120)
2. **Select Gender** (Female/Male/Other)

### In the Main Area:
1. **Select Fever Level:** None / Low / High
2. **Select Cough Type:** None / Dry / Wet / Blood
3. **Check Symptoms:** (Click checkboxes)
   - [ ] Shortness of breath
   - [ ] Wheezing
   - [ ] Chest pain
   - [ ] Fatigue
   - [ ] Loss of taste or smell
4. **Smoking History:** Yes / No

### Click "Diagnose" Button

### See Results:
- **Top 2 Diseases** with confidence percentages
- **Recommendation** based on diagnosis confidence
- **Explanation** of how scoring works

---

## ⚠️ Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```powershell
pip install -r requirements.txt
```

### Problem: Browser doesn't open automatically

**Solution:** Go to `http://localhost:8501` in your browser manually

### Problem: "Port 8501 already in use"

**Solution:** Use a different port
```powershell
streamlit run app.py --server.port 8502
```

### Problem: Python command not recognized

**Solution:** Ensure Python is installed. Check with:
```powershell
python --version
```

Should show Python 3.8 or higher.

---

## 📋 Quick Reference

| Task | Command | Purpose |
|------|---------|---------|
| **Install** | `pip install -r requirements.txt` | One-time setup |
| **Run App** | `streamlit run app.py` | Interactive web interface |
| **Test** | `python inference_engine.py` | Console verification test |
| **View KB** | `python knowledge_base.py` | See all diseases & symptoms |
| **Check Python** | `python --version` | Verify Python 3.8+ installed |

---

## 🔄 Typical Workflow for Grading

1. **Show it works:**
   ```powershell
   python inference_engine.py
   ```
   ✅ Shows system reasons correctly

2. **Show the knowledge base:**
   ```powershell
   python knowledge_base.py
   ```
   ✅ Shows 6 diseases and symptom knowledge

3. **Run the interactive app:**
   ```powershell
   streamlit run app.py
   ```
   ✅ Shows professional UI and user interaction

4. **Read the documentation:**
   - Open `README.md` - Project overview
   - Open `help.md` - Detailed guide
   - Read code comments in Python files

---

## 📂 Files in Your Project

```
TES-Project/
├── app.py                    ← Streamlit UI (run with: streamlit run app.py)
├── inference_engine.py       ← Reasoning logic (run with: python inference_engine.py)
├── knowledge_base.py         ← Disease rules (run with: python knowledge_base.py)
├── verify_run.py             ← Test runner (run with: python verify_run.py)
├── requirements.txt          ← Dependencies (install with: pip install -r requirements.txt)
├── README.md                 ← Project overview (READ THIS FIRST)
├── help.md                   ← Detailed usage guide
├── QUICK_START.md            ← Quick reference
├── PROJECT_SUMMARY.md        ← Completion checklist
└── RUN_GUIDE.md             ← This file
```

---

## ✅ Success Checklist

- ✅ Python 3.8+ installed: `python --version`
- ✅ Dependencies installed: `pip list | findstr streamlit`
- ✅ Verification test passes: `python inference_engine.py`
- ✅ Web app launches: `streamlit run app.py`
- ✅ Browser opens to http://localhost:8501
- ✅ Can enter symptoms and click Diagnose
- ✅ Sees top 2 diseases with percentages
- ✅ Code comments are visible in Python files

---

**Ready to run your expert system!** 🏥✨

For more details, see:
- **help.md** - Complete documentation
- **README.md** - Project overview
- **QUICK_START.md** - Quick reference
