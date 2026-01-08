from inference_engine import diagnose


def test_verification_case():
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

    results = diagnose(patient)
    # top result should be COVID-19 and score should be > 70
    assert results, "Expected non-empty results"
    top_disease, top_score = results[0]
    assert top_disease == "COVID-19"
    assert top_score >= 70
