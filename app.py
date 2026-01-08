"""
Streamlit User Interface for the Respiratory Disease Expert System

This module implements a simple, clean web UI according to the assignment
requirements. The UI is split into a sidebar for demographics and a main area
for symptom inputs. Pressing the "Diagnose" button runs the inference engine
and displays the top two likely diseases with recommendations.
"""

import streamlit as st
from inference_engine import diagnose


def main():
    st.set_page_config(page_title="Respiratory Diagnosis Expert System")

    st.title("Rule-Based Respiratory Disease Diagnosis")

    # Sidebar: patient demographics
    st.sidebar.header("Patient Information")
    age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=35)
    gender = st.sidebar.selectbox("Gender", ["Female", "Male", "Other"])

    # Main area: symptom inputs
    st.header("Symptoms")

    fever = st.radio("Fever", ("none", "low", "high"))

    cough = st.radio("Cough type", ("none", "dry", "wet", "blood"))

    shortness_of_breath = st.checkbox("Shortness of breath")
    wheezing = st.checkbox("Wheezing")
    chest_pain = st.checkbox("Chest pain")
    fatigue = st.checkbox("Fatigue")
    loss_taste_smell = st.checkbox("Loss of taste or smell")

    smoking_history = st.selectbox("Smoking history", ["No", "Yes"]) == "Yes"

    # Prepare patient profile for inference
    patient_profile = {
        "age": age,
        "gender": gender,
        "fever": fever,
        "cough": cough if cough != "none" else None,
        "shortness_of_breath": shortness_of_breath,
        "wheezing": wheezing,
        "chest_pain": chest_pain,
        "fatigue": fatigue,
        "loss_taste_smell": loss_taste_smell,
        "smoking_history": smoking_history,
    }

    if st.button("Diagnose"):
        # Run inference
        results = diagnose(patient_profile)

        # Show top 2 diseases
        st.subheader("Top diagnoses")
        if not results:
            st.write("No results produced. Check inputs.")
            return

        top2 = results[:2]
        for disease, score in top2:
            st.write(f"**{disease}**: {score}% match")

        # Simple recommendations based on highest score
        best_disease, best_score = results[0]
        st.subheader("Recommendation")
        if best_score >= 75:
            st.info(f"High likelihood of {best_disease}. Recommend seeing a pulmonologist promptly.")
        elif best_score >= 40:
            st.warning(f"Possible {best_disease}. Consider primary care consultation and further testing.")
        else:
            st.success("Low match for the measured respiratory diseases. Monitor symptoms and seek care if they worsen.")

        # Display a short rationale for the top result
        st.subheader("Explanation (brief)")
        st.write("This expert system uses weighted rules (certainty factors). The displayed "
                 "percentages are normalised scores based on how well the entered symptoms "
                 "match disease profiles in the knowledge base.")


if __name__ == "__main__":
    main()
