"""
Streamlit User Interface for the Respiratory Disease Expert System

This module implements a beautiful, professional web UI with a cute medical
cartoon aesthetic. The interface is split into a sidebar for patient demographics
and a main area for symptom inputs. The "Diagnose" button runs the inference
engine and displays the top diagnoses with color-coded recommendations.
"""

import streamlit as st
from inference_engine import diagnose

# Configure page with custom styling
st.set_page_config(
    page_title="🏥 Respiratory Diagnosis System",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalist HCI-compliant styling
st.markdown("""
    <style>
    /* Clean minimalist color scheme */
    :root {
        --primary: #0066CC;
        --secondary: #F0F2F5;
        --border: #DADCE0;
        --text-primary: #202124;
        --text-secondary: #5F6368;
        --success: #1E8449;
        --warning: #D68910;
        --info: #2874A6;
    }
    
    /* Minimalist background */
    .stApp {
        background: #FFFFFF;
    }
    /* Force readable text color across Streamlit components */
    .stApp, .stApp * {
        color: #202124 !important;
    }
    
    /* Clean container styling */
    .main-container {
        padding: 20px;
        max-width: 1000px;
    }
    
    /* Header - clean and simple */
    .header-container {
        padding: 24px 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 32px;
    }
    
    .header-title {
        color: #202124;
        font-size: 28px;
        font-weight: 500;
        margin: 0;
        line-height: 1.3;
    }
    
    .header-subtitle {
        color: #5F6368;
        font-size: 14px;
        margin-top: 4px;
    }
    
    /* Clean card layout */
    .input-section {
        background: var(--secondary);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 20px;
        margin: 16px 0;
    }
    
    .section-title {
        color: #202124;
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 16px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Result cards - clean design */
    .result-item {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .disease-info {
        flex: 1;
    }
    
    .disease-title {
        color: #202124;
        font-size: 16px;
        font-weight: 600;
        margin: 0;
    }
    
    .disease-label {
        color: var(--text-secondary);
        font-size: 12px;
        margin: 4px 0 0 0;
    }
    
    .score-display {
        text-align: right;
        min-width: 80px;
    }
    
    .score-number {
        color: var(--primary);
        font-size: 32px;
        font-weight: 600;
        margin: 0;
        line-height: 1;
    }
    
    .score-label {
        color: var(--text-secondary);
        font-size: 12px;
        margin-top: 4px;
    }
    
    /* Progress bar - minimal */
    .progress-bar {
        height: 4px;
        background: var(--secondary);
        border-radius: 2px;
        margin-top: 8px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: var(--primary);
        border-radius: 2px;
        transition: width 0.3s ease;
    }
    
    /* Button styling - clean */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
        width: 100%;
        transition: background 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #0052A3;
    }
    
    /* Recommendation boxes */
    .recommendation-high {
        background: #F1F8E9;
        border-left: 4px solid var(--success);
        padding: 16px;
        border-radius: 4px;
        margin: 16px 0;
    }
    
    .recommendation-medium {
        background: #FFF3E0;
        border-left: 4px solid var(--warning);
        padding: 16px;
        border-radius: 4px;
        margin: 16px 0;
    }
    
    .recommendation-low {
        background: #E3F2FD;
        border-left: 4px solid var(--info);
        padding: 16px;
        border-radius: 4px;
        margin: 16px 0;
    }
    
    .recommendation-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 14px;
        margin: 0 0 8px 0;
    }
    
    .recommendation-text {
        color: var(--text-secondary);
        font-size: 13px;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: #FFFFFF;
        border-right: 1px solid var(--border);
    }
    
    /* Clean input spacing */
    .input-group {
        margin-bottom: 16px;
    }
    
    .input-label {
        color: #202124;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
        display: block;
    }
    
    /* Footer */
    .footer {
        border-top: 1px solid var(--border);
        padding: 24px 0;
        margin-top: 40px;
        text-align: center;
        color: var(--text-secondary);
        font-size: 12px;
    }
    
    /* Responsive layout */
    @media (max-width: 768px) {
        .result-item {
            flex-direction: column;
            align-items: flex-start;
        }
        
        .score-display {
            margin-top: 12px;
            text-align: left;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    # Clean minimalist header
    st.markdown("""
    <div class='header-container'>
        <h1 class='header-title'>Respiratory Disease Diagnosis</h1>
        <p class='header-subtitle'>Evidence-based diagnostic assistant system</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar: patient demographics - minimalist
    with st.sidebar:
        st.markdown("<div class='header-container'><h2 class='section-title'>Patient Information</h2></div>", unsafe_allow_html=True)
        
        age = st.slider(
            "Age",
            min_value=0,
            max_value=120,
            value=35,
            help="Patient age in years"
        )
        
        gender = st.selectbox(
            "Gender",
            ["Female", "Male", "Other"],
            help="Patient gender"
        )

    # Main content area
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # Symptom input section
    st.markdown("<h2 class='section-title'>Symptom Assessment</h2>", unsafe_allow_html=True)
    
    # Organized input layout
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<label class='input-label'>Fever Status</label>", unsafe_allow_html=True)
        fever = st.radio(
            "Select fever level:",
            ("None", "Low", "High"),
            horizontal=True,
            label_visibility="collapsed"
        )
        fever_value = "none" if fever == "None" else fever.lower()
    
    with col2:
        st.markdown("<label class='input-label'>Cough Type</label>", unsafe_allow_html=True)
        cough = st.radio(
            "Select cough type:",
            ("None", "Dry", "Wet", "Blood"),
            horizontal=True,
            label_visibility="collapsed"
        )
        cough_value = "none" if cough == "None" else cough.lower()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional options
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("<label class='input-label'>Smoking History</label>", unsafe_allow_html=True)
    smoking_history = st.selectbox(
        "Smoking history:",
        ["No", "Yes"],
        label_visibility="collapsed"
    ) == "Yes"
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Symptoms checkboxes
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("<label class='input-label'>Additional Symptoms</label>", unsafe_allow_html=True)
    
    sym_col1, sym_col2, sym_col3 = st.columns(3)
    
    with sym_col1:
        shortness_of_breath = st.checkbox("Shortness of Breath")
        wheezing = st.checkbox("Wheezing")
    
    with sym_col2:
        chest_pain = st.checkbox("Chest Pain")
        fatigue = st.checkbox("Fatigue")
    
    with sym_col3:
        loss_taste_smell = st.checkbox("Loss of Taste/Smell")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Prepare patient profile for inference
    patient_profile = {
        "age": age,
        "gender": gender,
        "fever": fever_value,
        "cough": cough_value if cough_value != "none" else None,
        "shortness_of_breath": shortness_of_breath,
        "wheezing": wheezing,
        "chest_pain": chest_pain,
        "fatigue": fatigue,
        "loss_taste_smell": loss_taste_smell,
        "smoking_history": smoking_history,
    }

    # Diagnosis button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        diagnose_button = st.button("Analyze Symptoms", key="diagnose_btn", use_container_width=True)

    if diagnose_button:
        # Run inference
        results = diagnose(patient_profile)

        if not results:
            st.error("Unable to process input. Please check your entries.")
            return

        # Results section
        st.markdown("<h2 class='section-title'>Diagnosis Results</h2>", unsafe_allow_html=True)
        
        top2 = results[:2]
        
        # Display top 2 results in clean cards
        for idx, (disease, score) in enumerate(top2, 1):
            st.markdown(f"""
            <div class='result-item'>
                <div class='disease-info'>
                    <h3 class='disease-title'>{disease}</h3>
                    <p class='disease-label'>Rank: #{idx} of {len(results)} diseases</p>
                    <div class='progress-bar'>
                        <div class='progress-fill' style='width: {score}%'></div>
                    </div>
                </div>
                <div class='score-display'>
                    <p class='score-number'>{score}%</p>
                    <p class='score-label'>Confidence</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Recommendations
        st.markdown("<h2 class='section-title'>Clinical Recommendation</h2>", unsafe_allow_html=True)
        
        best_disease, best_score = results[0]
        
        if best_score >= 75:
            st.markdown(f"""
            <div class='recommendation-high'>
                <h4 class='recommendation-title'>High Confidence Match</h4>
                <p class='recommendation-text'>
                    <strong>Primary Diagnosis:</strong> {best_disease}<br>
                    <strong>Recommendation:</strong> Schedule consultation with pulmonologist for confirmation and treatment plan.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif best_score >= 40:
            st.markdown(f"""
            <div class='recommendation-medium'>
                <h4 class='recommendation-title'>Moderate Confidence Match</h4>
                <p class='recommendation-text'>
                    <strong>Possible Diagnosis:</strong> {best_disease}<br>
                    <strong>Recommendation:</strong> Consult primary care physician for further evaluation and testing.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='recommendation-low'>
                <h4 class='recommendation-title'>Low Confidence Match</h4>
                <p class='recommendation-text'>
                    <strong>Weak Match:</strong> {best_disease}<br>
                    <strong>Recommendation:</strong> Continue symptom monitoring. Seek medical care if symptoms persist or worsen.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # System information
        st.markdown("<h2 class='section-title'>How This Works</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class='input-section'>
            <p style='color: var(--text-secondary); font-size: 13px; line-height: 1.6; margin: 0;'>
                This system applies weighted medical rules (certainty factors) to analyze entered symptoms 
                and calculate diagnosis confidence scores. Percentages represent how well your symptom profile 
                matches known disease patterns in the medical knowledge base.
            </p>
            <p style='color: #D32F2F; font-size: 12px; margin: 12px 0 0 0;'>
                Medical Disclaimer: For educational purposes only. Consult healthcare providers for professional medical diagnosis.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class='footer'>
        <p>Respiratory Disease Expert System | Version 1.0</p>
        <p>Evidence-based diagnostic assistant for educational purposes</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
