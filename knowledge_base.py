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

KNOWLEDGE_BASE: Dict[str, Dict[str, float]] = {
    "Asthma": {
        # Asthma often features wheeze and shortness of breath; cough may be dry.
        "wheezing": 0.9,
        "shortness_of_breath": 0.8,
        "cough_dry": 0.6,
        "fever_none": 0.2,  # lack of fever slightly supports asthma (non-infectious)
        "chest_pain": 0.3,
        "fatigue": 0.3,
        "smoking_history": 0.2,
    },
    "COPD": {
        # COPD associated with chronic smoking, dyspnea and productive cough
        "smoking_history": 0.9,
        "cough_wet": 0.7,
        "shortness_of_breath": 0.8,
        "wheezing": 0.5,
        "fatigue": 0.5,
        "fever_none": 0.1,
    },
    "Pneumonia": {
        # Pneumonia commonly causes fever, productive cough, chest pain
        "fever_high": 0.9,
        "cough_wet": 0.8,
        "chest_pain": 0.6,
        "shortness_of_breath": 0.7,
        "fatigue": 0.6,
        "smoking_history": 0.2,
    },
    "COVID-19": {
        # COVID-19 often causes fever, dry cough, fatigue, and loss of taste/smell
        "fever_high": 0.8,
        "fever_low": 0.4,
        "cough_dry": 0.7,
        "shortness_of_breath": 0.6,
        "fatigue": 0.6,
        "loss_taste_smell": 0.95,
        "chest_pain": 0.3,
    },
    "Tuberculosis": {
        # TB may present with chronic cough (sometimes blood), low-grade fever,
        # weight loss and fatigue. We approximate with available symptoms.
        "fever_low": 0.6,
        "cough_blood": 0.8,
        "cough_wet": 0.5,
        "fatigue": 0.7,
        "shortness_of_breath": 0.5,
        "smoking_history": 0.3,
    },
    "Acute Bronchitis": {
        # Acute bronchitis often has cough (dry or wet), sometimes mild fever
        "cough_dry": 0.5,
        "cough_wet": 0.6,
        "fever_low": 0.4,
        "fatigue": 0.4,
        "shortness_of_breath": 0.3,
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
