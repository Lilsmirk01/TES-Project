Design Document: Rule-Based Respiratory Diagnosis Expert System

Overview
- Domain: Respiratory diseases (educational prototype)
- Approach: Rule-based expert system using IF–THEN rules with Certainty Factors (CF)
- Reasoning: Forward chaining

Knowledge Representation
- Each disease is represented by a set of symptom rules.
- Each rule contains:
  - `cf` (float 0.0-1.0): expert-assigned certainty factor
  - `explain` (string): short justification of the rule
- Multi-valued symptoms are encoded as separate keys (e.g., `fever_high`).

Inference Engine
- For each disease:
  1. Sum CFs for symptoms present in the patient profile.
  2. Subtract penalties for expected-but-absent symptoms (penalty fraction = 0.5).
  3. Normalise by the sum of positive CFs for the disease to produce a percentage.
- `diagnose_with_explanation()` returns a structured trace showing matched
  evidence and penalties for explainability.

Explainability
- Every rule includes a human-readable explanation string.
- The inference engine returns `matched` and `penalties` lists for each disease,
  enabling transparent reporting of why a diagnosis was ranked highly.

Design Rationale
- Simplicity and explainability prioritized for academic evaluation.
- No machine learning; all weights are expert-encoded CFs and documented.

Files
- `knowledge_base.py`: holds the CF-based rules and explanations.
- `inference_engine.py`: forward-chaining engine + explain function.
- `app.py`: Streamlit UI that displays results and explanations.

Ethics & Limitations
- Educational prototype only; not medical advice. See DISCLAIMER.md for full text.