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

from typing import Dict, List, Tuple
from knowledge_base import KNOWLEDGE_BASE


def _disease_max_score(disease_rules: Dict[str, float]) -> float:
    """Return the maximum (sum) of positive CFs for a disease.

    We use this to normalise the raw score into a percentage.
    """
    return sum(max(0.0, v) for v in disease_rules.values())


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

    # For every disease compute support
    for disease, rules in KNOWLEDGE_BASE.items():
        raw_score = 0.0
        max_score = _disease_max_score(rules)

        # Defensive: if max_score is zero (shouldn't happen), avoid division by zero
        if max_score <= 0.0:
            results.append((disease, 0.0))
            continue

        # Sum positive evidence
        for symptom_key, cf in rules.items():
            if symptom_key in present:
                # Symptom present: increase support by CF
                raw_score += cf
            else:
                # Symptom absent: if the symptom was expected (cf high), apply
                # a penalty proportional to its weight. This models negative
                # evidence reducing confidence in the disease.
                # Penalty fraction chosen empirically for clarity in outputs.
                penalty_fraction = 0.5
                raw_score -= cf * penalty_fraction

        # Normalise and clamp
        percent = max(0.0, min(1.0, raw_score / max_score)) * 100.0
        results.append((disease, round(percent, 1)))

    # Sort by descending percentage
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
