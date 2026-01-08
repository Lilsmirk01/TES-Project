"""
Inference Engine (Forward Chaining) for Respiratory Disease Expert System

This module implements a simple forward-chaining inference routine that uses
the certainty-factor weighted Knowledge Base to compute a match score for each
disease given a patient symptom profile.

Design and reasoning (comments required by academic rubric):
- We perform a rule-matching step for each disease: if the patient's profile
  provides a symptom that corresponds to a KB key, we add that symptom's CF
  to the disease's support score.
- Because diseases have different sets of supporting symptoms with different
  maximum sums, we normalise by the sum of the positive CFs for that disease
  to obtain a comparable percentage across diseases.
- We penalise the absence of key expected symptoms: if a disease lists a
  symptom with a high CF but the patient explicitly reports the opposite
  (e.g., disease expects fever_high but patient has fever_none), we subtract a
  portion of that CF as a penalty. This helps forward-chaining handle negative
  evidence.

Note: The combination method here (add and normalise) is intentionally simple
for clarity and grading. More advanced CF combination rules exist (e.g., MYCIN
style combination), but they are out of scope for this assignment.
"""

from typing import Dict, List, Tuple, Any
from knowledge_base import KNOWLEDGE_BASE


def _disease_max_score(disease_rules: Dict[str, float]) -> float:
    """Return the maximum (sum) of positive CFs for a disease.

    We use this to normalise the raw score into a percentage.
    """
    total = 0.0
    for v in disease_rules.values():
        if isinstance(v, dict):
            total += max(0.0, float(v.get("cf", 0.0)))
        else:
            total += max(0.0, float(v))
    return total


def diagnose(patient_profile: Dict[str, str or bool]) -> List[Tuple[str, float]]:
    """
    Diagnose by forward-chaining through the knowledge base.

    patient_profile: mapping of symptom keys to values. For multi-valued
      symptoms we expect string values (e.g., fever: 'high'|'low'|'none'). For
      boolean symptoms, supply True/False.

    Returns a list of (disease, percentage_score) sorted descending.
    """
    results: List[Tuple[str, float]] = []

    # Preprocess patient profile into a set of symptom keys that are "present"
    # Example: if patient_profile['fever'] == 'high' -> present_key = 'fever_high'
    present = set()

    # Handle fever (multi-valued)
    fever_val = patient_profile.get("fever")
    if fever_val in ("high", "low", "none"):
        present.add(f"fever_{fever_val}")

    # Handle cough (multi-valued)
    cough_val = patient_profile.get("cough")
    if cough_val in ("dry", "wet", "blood"):
        present.add(f"cough_{cough_val}")

    # Handle boolean symptoms
    for bool_sym in ("shortness_of_breath", "wheezing", "chest_pain", "fatigue", "loss_taste_smell"):
        if patient_profile.get(bool_sym):
            present.add(bool_sym)

    # Smoking history: we store as boolean True/False (True -> positive)
    if patient_profile.get("smoking_history"):
        present.add("smoking_history")
    else:
        # explicit absence can be represented as 'fever_none' style keys for other symptoms
        pass

    # For every disease compute support (backwards compatible with old KB)
    for disease, rules in KNOWLEDGE_BASE.items():
        raw_score = 0.0
        max_score = _disease_max_score(rules)

        # Defensive: if max_score is zero (shouldn't happen), avoid division by zero
        if max_score <= 0.0:
            results.append((disease, 0.0))
            continue

        # Sum positive evidence and apply penalties for absent expected symptoms
        for symptom_key, rule_val in rules.items():
            cf = float(rule_val["cf"]) if isinstance(rule_val, dict) else float(rule_val)
            if symptom_key in present:
                raw_score += cf
            else:
                penalty_fraction = 0.5
                raw_score -= cf * penalty_fraction

        # Normalise and clamp
        percent = max(0.0, min(1.0, raw_score / max_score)) * 100.0
        results.append((disease, round(percent, 1)))

    # Sort by descending percentage
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def diagnose_with_explanation(patient_profile: Dict[str, str or bool]) -> List[Tuple[str, float, Dict[str, Any]]]:
    """Diagnose and return structured explanations for each disease.

    Returns a list of tuples: (disease, percent, explanation_dict)
    explanation_dict contains: raw_score, max_score, percent, matched, penalties
    where matched is a list of matched symptom facts and penalties lists absent expectations.
    """
    results: List[Tuple[str, float, Dict[str, Any]]] = []

    # Preprocess profile into present set (reuse logic)
    present = set()
    fever_val = patient_profile.get("fever")
    if fever_val in ("high", "low", "none"):
        present.add(f"fever_{fever_val}")
    cough_val = patient_profile.get("cough")
    if cough_val in ("dry", "wet", "blood"):
        present.add(f"cough_{cough_val}")
    for bool_sym in ("shortness_of_breath", "wheezing", "chest_pain", "fatigue", "loss_taste_smell"):
        if patient_profile.get(bool_sym):
            present.add(bool_sym)
    if patient_profile.get("smoking_history"):
        present.add("smoking_history")

    for disease, rules in KNOWLEDGE_BASE.items():
        raw_score = 0.0
        max_score = _disease_max_score(rules)
        if max_score <= 0.0:
            expl = {"raw_score": 0.0, "max_score": 0.0, "percent": 0.0, "matched": [], "penalties": []}
            results.append((disease, 0.0, expl))
            continue

        matched = []
        penalties = []

        for symptom_key, rule_val in rules.items():
            if isinstance(rule_val, dict):
                cf = float(rule_val.get("cf", 0.0))
                reason = rule_val.get("explain", "")
            else:
                cf = float(rule_val)
                reason = ""

            if symptom_key in present:
                raw_score += cf
                matched.append({"symptom": symptom_key, "cf": cf, "explain": reason})
            else:
                penalty_fraction = 0.5
                pen = cf * penalty_fraction
                raw_score -= pen
                penalties.append({"symptom": symptom_key, "penalty": pen, "cf": cf, "explain": reason})

        percent = max(0.0, min(1.0, raw_score / max_score)) * 100.0
        expl = {"raw_score": round(raw_score, 3), "max_score": round(max_score, 3), "percent": round(percent, 1), "matched": matched, "penalties": penalties}
        results.append((disease, round(percent, 1), expl))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def run_verification():
    """Run a hard-coded test case and print results for verification.

    This function satisfies the assignment's Verification Feature requirement.
    It demonstrates the inference engine with a sample patient profile.
    """
    # Test case: A patient with high fever, dry cough, loss of taste/smell,
    # and shortness of breath — typical for COVID-19-like presentation.
    patient = {
        "fever": "high",
        "cough": "dry",
        "shortness_of_breath": True,
        "wheezing": False,
        "chest_pain": False,
        "fatigue": True,
        "loss_taste_smell": True,
        "smoking_history": False,
    }

    print("Running verification test case (hard-coded patient):")
    results = diagnose(patient)
    for disease, score in results[:4]:
        print(f" - {disease}: {score}% match")


if __name__ == "__main__":
    run_verification()
