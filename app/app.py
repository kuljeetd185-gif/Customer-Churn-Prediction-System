import streamlit as st
import plotly.graph_objects as go
import pickle
import pandas as pd
import os
import streamlit.components.v1 as components
import time 

# -------------------------------
# TEXT TO SPEECH FUNCTION
# -------------------------------
def speak_text(text):
    
    js_code = f"""
    <script>

    function speakNow() {{

        let voices = window.speechSynthesis.getVoices();

        let msg = new SpeechSynthesisUtterance();

        msg.text = `{text}`;

        // PROFESSIONAL VOICE SETTINGS
        msg.rate = 1.02;

        msg.pitch = 0.92;

        msg.volume = 1;

        // PREMIUM VOICE PRIORITY
        msg.voice =
            voices.find(v => v.name.includes("Google UK English Female")) ||
            voices.find(v => v.name.includes("Microsoft Aria")) ||
            voices.find(v => v.name.includes("Samantha")) ||
            voices.find(v => v.name.includes("Jenny")) ||
            voices[0];

        // REMOVE PREVIOUS SPEECH
        window.speechSynthesis.cancel();

        // SPEAK
        window.speechSynthesis.speak(msg);
    }}

    // LOAD VOICES PROPERLY
    speechSynthesis.onvoiceschanged = speakNow;

    // FALLBACK
    speakNow();

    </script>
    """


    components.html(js_code, height=0)
  

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Churn Dashboard", layout="wide")

# ---------------------------------
# SPLASH SCREEN ONLY ON FIRST LOAD
# ---------------------------------

import time

if "splash_shown" not in st.session_state:

    st.session_state.splash_shown = False

if not st.session_state.splash_shown:

    splash_placeholder = st.empty()

    splash_placeholder.markdown(
        """
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 999999;
        ">

        <div style="
                color: white;
                font-size: 70px;
                font-weight: 700;
                letter-spacing: 5px;
                font-family: 'Segoe UI', sans-serif;
        ">
                Rentenza AI
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(" ")

    time.sleep(2.5)

    splash_placeholder.empty()

    st.session_state.splash_shown = True


# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    color: white;
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    margin-bottom: 15px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}


.metric-card {
    background: rgba(255,255,255,0.14);

    padding: 25px;

    border-radius: 24px;

    text-align: center;

    border: 1px solid rgba(255,255,255,0.20);

    box-shadow: 0 8px 25px rgba(0,0,0,0.30);

    min-height: 220px;

    width: 100%;

    display: flex;
    flex-direction: column;

    justify-content: center;

    align-items: center;

    transition: all 0.35s ease;

    backdrop-filter: blur(12px);
}

/* Hover Effect */
.metric-card:hover {

    transform: scale(1.06) translateY(-6px);

    background: rgba(255,255,255,0.20);

    box-shadow:
        0 15px 35px rgba(0,0,0,0.40),
        0 0 20px rgba(0,198,255,0.5);

    cursor: pointer;
}

.metric-card h4 {
    font-size: 22px;
    margin-bottom: 12px;
}

.metric-card h2 {
    font-size: 40px;
    margin-bottom: 12px;
    color: #00c6ff;
}

.metric-card p {
    font-size: 15px;
    line-height: 1.5;
}
.speaking-box {

    background: rgba(0,198,255,0.12);

    border: 2px solid #00c6ff;

    padding: 25px;

    border-radius: 20px;

    color: white;

    font-size: 18px;

    line-height: 1.8;

    animation: glowPulse 1.5s infinite;

    box-shadow:
        0 0 15px rgba(0,198,255,0.5),
        0 0 35px rgba(0,198,255,0.4);

    transition: all 0.3s ease;
}

/* Glow Animation */

@keyframes glowPulse {

    0% {
        box-shadow:
            0 0 10px rgba(0,198,255,0.4),
            0 0 20px rgba(0,198,255,0.2);
    }

    50% {
        box-shadow:
            0 0 25px rgba(0,198,255,0.9),
            0 0 50px rgba(0,198,255,0.6);
    }

    100% {
        box-shadow:
            0 0 10px rgba(0,198,255,0.4),
            0 0 20px rgba(0,198,255,0.2);
    }
}



""", unsafe_allow_html=True)


# -------------------------------
# LOAD MODEL
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "churn_model.pkl"), "rb"))
features = pickle.load(open(os.path.join(BASE_DIR, "features.pkl"), "rb"))

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 Customer Churn Prediction Dashboard")
st.markdown("### Analyze and predict customer churn in real-time")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🧾 Customer Input")

tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 12)
monthly_charges = st.sidebar.number_input("Monthly Charges", 0.0, 200.0, 50.0)
total_charges = st.sidebar.number_input("Total Charges", 0.0, 10000.0, 500.0)

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
internet = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

st.sidebar.markdown("---")
st.sidebar.info("Built by Kuljeet Singh Dhillon 🚀")

# -------------------------------
# INPUT DATA
# -------------------------------
input_data = pd.DataFrame([[0]*len(features)], columns=features)

input_data["tenure"] = tenure
input_data["MonthlyCharges"] = monthly_charges
input_data["TotalCharges"] = total_charges

# Encoding
if "gender_Male" in input_data:
    input_data["gender_Male"] = 1 if gender == "Male" else 0

if "Contract_One year" in input_data:
    input_data["Contract_One year"] = 1 if contract == "One year" else 0

if "Contract_Two year" in input_data:
    input_data["Contract_Two year"] = 1 if contract == "Two year" else 0

if "InternetService_Fiber optic" in input_data:
    input_data["InternetService_Fiber optic"] = 1 if internet == "Fiber optic" else 0

if "InternetService_No" in input_data:
    input_data["InternetService_No"] = 1 if internet == "No" else 0

# -------------------------------
# KPI CARDS
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card'><h3>📅 Tenure</h3><h2>{tenure}</h2></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='card'><h3>💰 Monthly Charges</h3><h2>{monthly_charges}</h2></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='card'><h3>🌐 Internet</h3><h2>{internet}</h2></div>", unsafe_allow_html=True)

# -------------------------------
# PREDICTION
# -------------------------------

probability = None
prediction = None
insight_message = ""

if st.button("🚀 Analyze Customer"):

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

   # ---------------- INSIGHTS ----------------

    st.markdown("### 📊 AI Generated Customer Insights")

if probability is not None:

    if probability > 0.7:

        insight_message = """        
        The customer shows a high churn probability due to high monthly charges,
        shorter tenure duration, and lower long-term service commitment.
        Month-to-month subscription behavior further increases churn risk.

        Recommendation:
        Offer personalized retention discounts, loyalty rewards, and long-term
        subscription benefits. Proactive customer engagement and service support
        should be prioritized to improve retention probability.
        """

        st.error(insight_message)

    elif probability > 0.4:

        insight_message = """
        The customer demonstrates moderate churn tendencies influenced by pricing,
        engagement patterns, and subscription behavior. Reduced interaction levels
        may gradually increase churn probability over time.

        Recommendation:
        Strengthen customer engagement through personalized communication,
        promotional offers, and satisfaction-focused service improvements.
        Encouraging longer subscription plans may improve customer retention.
        """

        st.warning(insight_message)

    else:

        insight_message = """
        The customer currently shows stable retention behavior with healthy service
        engagement and satisfactory subscription activity. Lower churn indicators
        suggest strong customer stability.

        Recommendation:
        Maintain service quality and customer satisfaction standards while offering
        loyalty benefits and long-term engagement opportunities to preserve customer retention.
        """

        st.success(insight_message)

    # AUTO SPEAK
    speak_text(insight_message) 

    # ---------------- SPEAK BUTTON ----------------
    if st.button("🔊 Speak Insight"):
        speak_text(insight_message)

    if probability is not None:
    
    # Gauge Chart
     fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        title={'text': "Churn Probability (%)"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    st.plotly_chart(fig)

    # Bar Chart
    fig2 = go.Figure(data=[
        go.Bar(
            x=["Stay", "Churn"],
            y=[1 - probability, probability]
        )
    ])

    st.plotly_chart(fig2)
    
# -------------------------------
# SESSION STATE
# -------------------------------

if "show_evaluation" not in st.session_state:
    st.session_state["show_evaluation"] = False

# -------------------------------
# MODEL EVALUATION BUTTON
# -------------------------------

if st.button("📊 Model Evaluation"):
    st.session_state["show_evaluation"] = True

# -------------------------------
# SHOW EVALUATION ONLY AFTER CLICK
# -------------------------------

if st.session_state["show_evaluation"]:

    st.markdown("---")

    # TITLE
    st.markdown("## 🤖 AI Model Performance Dashboard")

    st.markdown("""
    Evaluate the predictive reliability and analytical performance
    of the machine learning model used for customer churn prediction.
    """)

    # -------------------------------
    # FIRST ROW KPI
    # -------------------------------

    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown("""
        <div class='metric-card'>
            <h4>🎯 Accuracy</h4>
            <h2>82.11%</h2>
            <p>Strong Overall Prediction</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(0.8211)

    with k2:
        st.markdown("""
        <div class='metric-card'>
            <h4>📌 Precision</h4>
            <h2>68.50%</h2>
            <p>Reliable Churn Detection</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(0.6850)

    with k3:
        st.markdown("""
        <div class='metric-card'>
            <h4>🔍 Recall</h4>
            <h2>60.05%</h2>
            <p>Effective Risk Identification</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(0.6005)

    # -------------------------------
    # SECOND ROW KPI
    # -------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    k4, k5 = st.columns(2)

    with k4:
        st.markdown("""
        <div class='metric-card'>
            <h4>⚖️ F1 Score</h4>
            <h2>64.00%</h2>
            <p>Balanced Classification Model</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(0.6400)

    with k5:
        st.markdown("""
        <div class='metric-card'>
            <h4>📈 ROC-AUC</h4>
            <h2>86.23%</h2>
            <p>Excellent Predictive Separation</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(0.8623)

        # -------------------------------
    # SPACING
    # -------------------------------

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()

    # -------------------------------
    # SUMMARY
    # -------------------------------

    evaluation_message = """
    The churn prediction model demonstrates strong predictive capability
    with reliable classification performance across customer churn scenarios.

    The achieved ROC-AUC score above 86 percent indicates excellent
    separation capability between churn and non-churn customers.

    Accuracy, precision, recall, and F1 metrics collectively confirm
    the model's analytical consistency and business reliability.
    """

    st.markdown("## 📌 Model Evaluation Summary")

    st.info(evaluation_message)

    # -------------------------------
    # SPEAK BUTTON
    # -------------------------------

    if st.button("🔊 Speak Evaluation Summary"):

        speak_text(evaluation_message)

# -------------------------------
# STATIC INSIGHTS
# -------------------------------

st.markdown("### 💡 Key Insights")

st.markdown("""
<div class='card'>
<ul>
<li>High monthly charges significantly increase churn probability.</li>
<li>Customers with lower tenure show higher disengagement behavior.</li>
<li>Month-to-month contract users represent the highest churn segment.</li>
<li>Long-term contracts contribute to improved customer retention.</li>
<li>Internet service type strongly influences churn behavior patterns.</li>
</ul>
</div>
""", unsafe_allow_html=True)