# Rule-Based Expert System for Respiratory Disease Diagnosis - Help Guide

## Overview

This project is a **Rule-Based Expert System (ES)** designed to diagnose respiratory diseases using a forward-chaining inference engine and a knowledge base of medical rules. The system is built with Python and Streamlit, following professional software architecture best practices.

### What It Does

The expert system takes a patient's reported symptoms and demographics, applies domain knowledge (encoded as certainty factors), and produces ranked diagnoses with confidence scores.

**Supported Diseases:**
- Asthma
- COPD (Chronic Obstructive Pulmonary Disease)
- Pneumonia
- COVID-19
- Tuberculosis
- Acute Bronchitis

---

## System Architecture

The project is split into **three independent modules** to demonstrate clean separation of concerns:

### 1. **knowledge_base.py** - Knowledge Representation
- Defines medical rules and symptoms in a Python dictionary
- Each disease is mapped to symptoms with associated **Certainty Factors (CF)** ranging from 0.0 to 1.0
- CF values represent expert confidence in the symptom-disease relationship
- **Why this design?** Dictionaries are human-readable, easy to inspect, extend, and serialize—ideal for academic evaluation
- **Symptoms tracked:** Fever, Cough, Shortness of Breath, Wheezing, Chest Pain, Fatigue, Loss of Taste/Smell, Smoking History

### 2. **inference_engine.py** - Logic & Reasoning
- Implements a **forward-chaining algorithm**
- Processes patient input and compares it against the knowledge base
- Calculates a match percentage for each disease
- Handles both positive evidence (symptoms present) and negative evidence (expected symptoms absent)
- Includes a **verification function** for testing (academic requirement)

### 3. **app.py** - User Interface (Streamlit)
- Clean, interactive web interface
- Sidebar: Patient demographics (Age, Gender)
- Main area: Symptom checkboxes and radio buttons
- Results: Top 2 diseases with confidence scores
- Recommendations: Medical advice based on diagnosis confidence

---

## Installation & Setup

### Prerequisites
- **Python 3.8 or higher**
- **pip** (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd path/to/TES-Project
```

### Step 2: Install Dependencies
Run this command in PowerShell or Command Prompt:

```bash
pip install -r requirements.txt
```

If you want to install packages individually:
```bash
pip install streamlit>=1.28.0
```

### Step 3: Verify Installation
Check that Streamlit is installed:
```bash
streamlit --version
```

Expected output: `Streamlit, version X.XX.X`

---

## Running the Application

### Option 1: Run the Web Interface (Recommended)

Navigate to the project directory and execute:

```bash
streamlit run app.py
```

**What to expect:**
- Streamlit will start a local server (typically `http://localhost:8501`)
- Your default browser will open automatically
- If not, manually open `http://localhost:8501` in your browser

**To stop the server:** Press `Ctrl+C` in PowerShell/Terminal

---

### Option 2: Run the Verification Test (Console)

To test the inference engine with a hard-coded patient profile:

```bash
python inference_engine.py
```

**Output example:**
```
Running verification test case (hard-coded patient):
 - COVID-19: 93.2% match
 - Pneumonia: 72.5% match
 - Asthma: 41.0% match
 - COPD: 28.3% match
```

---

### Option 3: Inspect the Knowledge Base

To view all defined diseases and symptoms:

```bash
python knowledge_base.py
```

---

## Using the Expert System

### Step-by-Step Walkthrough

1. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

2. **Enter Patient Information (Sidebar):**
   - Age: Numeric input (0-120)
   - Gender: Select from Female/Male/Other

3. **Report Symptoms (Main Area):**
   - **Fever:** Radio button (None / Low / High)
   - **Cough Type:** Radio button (None / Dry / Wet / Blood)
   - **Checkboxes** for:
     - Shortness of breath
     - Wheezing
     - Chest pain
     - Fatigue
     - Loss of taste or smell
   - **Smoking History:** Yes / No

4. **Click "Diagnose"** button

5. **Review Results:**
   - Top 2 diseases with confidence percentages
   - Color-coded recommendations:
     - 🔴 **75%+:** High likelihood—see a pulmonologist promptly
     - 🟡 **40-75%:** Possible diagnosis—consider primary care
     - 🟢 **Below 40%:** Low match—monitor and seek care if worsens

---

## How the Inference Engine Works

### Forward-Chaining Process

1. **Input Parsing:** Convert user input (symptoms) into a set of keys
   - Example: `fever: "high"` → key: `fever_high`

2. **Rule Matching:** For each disease in the knowledge base:
   - If patient has a symptom → add its certainty factor to the score
   - If patient lacks an expected symptom → subtract a penalty

3. **Normalization:** Convert raw score to a percentage (0-100%)
   ```
   percentage = (raw_score / max_possible_score) × 100
   ```

4. **Ranking:** Sort diseases by descending confidence and return top results

### Example Calculation

**Patient Profile:**
```
fever: high, cough: dry, fatigue: yes, loss_taste_smell: yes
```

**COVID-19 Rules (from KB):**
```
fever_high: 0.8, cough_dry: 0.7, fatigue: 0.6, loss_taste_smell: 0.95
```

**Calculation:**
- fever_high present → +0.8
- cough_dry present → +0.7
- fatigue present → +0.6
- loss_taste_smell present → +0.95
- **Raw score:** 3.05
- **Max possible:** 3.05 (all positive symptoms present)
- **Percentage:** (3.05 / 3.05) × 100 = **100%**

---

## Project Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI with patient input and results display |
| `inference_engine.py` | Forward-chaining algorithm and `diagnose()` function |
| `knowledge_base.py` | Disease-symptom rules with certainty factors |
| `requirements.txt` | Python dependencies |
| `README.md` | Project overview and academic requirements |
| `help.md` | This file—detailed usage and architecture guide |
| `verify_run.py` | Optional: standalone verification script |

---

## Academic Requirements Satisfied

✅ **Modular Architecture:** Three clearly separated modules (KB, Inference, UI)  
✅ **Knowledge Representation:** Dictionary-based with 6 diseases, 8+ symptoms, certainty factors  
✅ **Forward-Chaining:** Explicit rule-matching and evidence accumulation  
✅ **Interactive UI:** Streamlit interface with demographics, symptoms, results  
✅ **Extensive Comments:** All logic thoroughly documented with "why" explanations  
✅ **Verification Feature:** `run_verification()` function with hard-coded test case  
✅ **Negative Evidence Handling:** Absent symptoms reduce confidence scores  

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Run `pip install -r requirements.txt` in your project directory

### Issue: Streamlit app doesn't open a browser window
**Solution:** Manually navigate to `http://localhost:8501` in your browser

### Issue: "Port 8501 already in use"
**Solution:** Streamlit is already running. Either:
- Stop the existing process: `Ctrl+C`
- Run on a different port: `streamlit run app.py --server.port 8502`

### Issue: Python syntax error in app.py
**Solution:** Ensure Python 3.8+ is installed. Run `python --version` to check

### Issue: Symptoms don't affect diagnosis
**Solution:** Check that you've selected symptoms using checkboxes, and click the "Diagnose" button

---

## Extending the System

### Adding a New Disease

1. **Edit `knowledge_base.py`:**
   ```python
   KNOWLEDGE_BASE = {
       ...
       "My New Disease": {
           "fever_high": 0.8,
           "cough_wet": 0.7,
           # Add more symptom-CF pairs
       }
   }
   ```

2. **No changes needed** in `inference_engine.py` or `app.py` — they automatically adapt!

### Adjusting Certainty Factors

Modify the numeric values (0.0 - 1.0) in `KNOWLEDGE_BASE` to reflect domain expertise:
- `0.9 - 1.0`: Strong evidence for the disease
- `0.5 - 0.8`: Moderate evidence
- `0.1 - 0.4`: Weak evidence

---

## References & Background

- **Certainty Factors:** Shortliffe & Buchanan (MYCIN expert system)
- **Forward Chaining:** Production rule systems in AI
- **Streamlit:** Rapid prototyping framework for data apps

---

## Support

If you encounter issues, verify:
1. ✅ Python version (3.8+): `python --version`
2. ✅ Dependencies installed: `pip list | findstr streamlit`
3. ✅ All three source files exist in the project directory
4. ✅ No syntax errors: `python -m py_compile app.py inference_engine.py knowledge_base.py`

---

**Last Updated:** January 2026  
**Version:** 1.0  
**Status:** Production-Ready for Academic Submission
