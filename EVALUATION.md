Verification, Validation, and Evaluation

Verification (correctness of implementation)
- Unit tests for `diagnose()` and `diagnose_with_explanation()` using known
  patient-profiles with expected ranking outcomes.
- `inference_engine.run_verification()` provides a hard-coded sanity check.

Validation (clinical plausibility)
- Face validity: have clinical domain experts review rules and CF values.
- Case-based validation: compare outputs on clinical vignettes against
  textbook/clinical case expectations.

Evaluation metrics (academic)
- Ranking accuracy on curated case set (top-1/top-3 correctness)
- Explainability score: human raters judge whether the returned explanation
  includes the key supporting evidence.
- Sensitivity analysis: vary CFs +/- 10-20% and observe stability of rankings.

Recommended workflow for an assignment
1. Prepare a set of 20 representative vignettes with expert labels.
2. Run the system and record top-1/top-3 matches.
3. Report qualitative explanation examples and discuss failure modes.
4. Include an ethics section and limitations.

Notes
- This system is intentionally simple to illustrate expert-system principles.
- Avoid clinical claims; use aggregate, de-identified examples for evaluation.