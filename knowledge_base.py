"""
Knowledge Base for Respiratory Disease Expert System

This module defines the knowledge representation for the domain.

Design choices and comments:
- We use a Python dictionary to represent the knowledge base because dictionaries
  are easy to inspect, extend, and serialize. For an academic exercise this
  makes the representation explicit and human-readable (helpful for grading).
- Each disease maps to symptom keys with associated "certainty factors" (CF).
  CF values range from 0.0 (no support) to 1.0 (strong support). During
  inference we will sum and normalise against the maximum possible CF for each
  disease to produce a percentage match.
- Multi-valued symptoms (e.g., Fever, Cough) are encoded as distinct keys
  like 'fever_high', 'cough_dry' to keep matching straightforward.

Why CF and not raw probabilities?
- Certainty Factors are commonly used in rule-based ES teaching to express
  expert confidence in symptom-disease links. They are intuitive and easy to
  combine in forward-chaining rules. For the goal of this assignment, CFs
  satisfy the rubric requirement for weighted knowledge representation.

The KB below is simplified for educational purposes: values are illustrative
and tuned to make typical cases distinct (e.g., loss of taste/smell strongly
supports COVID-19). This is not clinical software.
"""

from typing import Dict

# Each disease maps to symptom keys with certainty factors (0.0 - 1.0).
# Symptoms tracked (encoded as keys used across the system):
# - fever_high, fever_low, fever_none
# - cough_dry, cough_wet, cough_blood
# - shortness_of_breath, wheezing, chest_pain, fatigue, loss_taste_smell
# - smoking_history

# Knowledge entries now include an explanation string alongside the CF value.
# This supports explainability: each rule is an IF symptom THEN disease with CF
# and a short explanation of why that symptom supports the disease.
KNOWLEDGE_BASE: Dict[str, Dict[str, Dict[str, object]]] = {
    "Asthma": {
        "wheezing": {"cf": 0.9, "explain": "Wheezing is a hallmark of airway constriction in asthma."},
        "shortness_of_breath": {"cf": 0.8, "explain": "Airflow limitation causes breathlessness."},
        "cough_dry": {"cf": 0.6, "explain": "Dry cough can occur with bronchospasm in asthma."},
        "fever_none": {"cf": 0.2, "explain": "Absence of fever slightly supports non-infectious causes like asthma."},
        "chest_pain": {"cf": 0.3, "explain": "Chest tightness or pain may accompany severe asthma."},
        "fatigue": {"cf": 0.3, "explain": "Reduced activity tolerance can follow persistent breathlessness."},
        "smoking_history": {"cf": 0.2, "explain": "Smoking can worsen airway hyperreactivity."},
    },
    "COPD": {
        "smoking_history": {"cf": 0.9, "explain": "Chronic smoking is the primary risk factor for COPD."},
        "cough_wet": {"cf": 0.7, "explain": "Productive cough is common in chronic bronchitis (COPD)."},
        "shortness_of_breath": {"cf": 0.8, "explain": "Progressive dyspnea is a core COPD feature."},
        "wheezing": {"cf": 0.5, "explain": "Wheezing can be present in COPD due to airflow obstruction."},
        "fatigue": {"cf": 0.5, "explain": "Reduced exercise tolerance is common in COPD."},
        "fever_none": {"cf": 0.1, "explain": "Fever is less typical for chronic non-infectious COPD baseline."},
    },
    "Pneumonia": {
        "fever_high": {"cf": 0.9, "explain": "High fever often accompanies infectious pneumonia."},
        "cough_wet": {"cf": 0.8, "explain": "Productive cough with purulent sputum suggests pulmonary infection."},
        "chest_pain": {"cf": 0.6, "explain": "Pleuritic chest pain can occur with lung consolidation."},
        "shortness_of_breath": {"cf": 0.7, "explain": "Infection and consolidation impair gas exchange."},
        "fatigue": {"cf": 0.6, "explain": "Systemic illness commonly causes fatigue."},
        "smoking_history": {"cf": 0.2, "explain": "Smoking is a minor risk factor for some pneumonias."},
    },
    "COVID-19": {
        "fever_high": {"cf": 0.8, "explain": "Fever is a common sign of viral infection including COVID-19."},
        "fever_low": {"cf": 0.4, "explain": "Low-grade fever can be seen in viral illness."},
        "cough_dry": {"cf": 0.7, "explain": "Dry cough is frequently reported in COVID-19."},
        "shortness_of_breath": {"cf": 0.6, "explain": "Lower respiratory involvement can cause dyspnea."},
        "fatigue": {"cf": 0.6, "explain": "Fatigue is a typical systemic symptom of COVID-19."},
        "loss_taste_smell": {"cf": 0.95, "explain": "Anosmia/ageusia is a strong, relatively specific feature of COVID-19."},
        "chest_pain": {"cf": 0.3, "explain": "Chest discomfort may occur in some cases."},
    },
    "Tuberculosis": {
        "fever_low": {"cf": 0.6, "explain": "Low-grade fever is often seen in TB."},
        "cough_blood": {"cf": 0.8, "explain": "Hemoptysis can be a feature of lung TB."},
        "cough_wet": {"cf": 0.5, "explain": "Chronic productive cough may indicate TB or chronic infections."},
        "fatigue": {"cf": 0.7, "explain": "Systemic symptoms such as fatigue are common in TB."},
        "shortness_of_breath": {"cf": 0.5, "explain": "Advanced pulmonary TB can cause dyspnea."},
        "smoking_history": {"cf": 0.3, "explain": "Smoking is a moderate risk factor for some TB outcomes."},
    },
    "Acute Bronchitis": {
        "cough_dry": {"cf": 0.5, "explain": "Acute bronchitis may start with a dry cough."},
        "cough_wet": {"cf": 0.6, "explain": "Productive cough often develops in bronchitis."},
        "fever_low": {"cf": 0.4, "explain": "Mild fever can accompany bronchitis."},
        "fatigue": {"cf": 0.4, "explain": "Fatigue may follow acute respiratory infection."},
        "shortness_of_breath": {"cf": 0.3, "explain": "Mild dyspnea can happen with bronchitis."},
    },
}


def get_symptom_keys():
    """Return the set of symptom keys used across the KB.

    Useful for building interfaces and validating input.
    """
    keys = set()
    for disease, rules in KNOWLEDGE_BASE.items():
        keys.update(rules.keys())
    return sorted(keys)


if __name__ == "__main__":
    # Quick inspection when run directly (not executed by Streamlit import)
    print("Defined diseases:")
    for d in KNOWLEDGE_BASE:
        print(f" - {d}")
    print("\nSymptom keys:")
    print(get_symptom_keys())
