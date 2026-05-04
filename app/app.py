import streamlit as st
import plotly.graph_objects as go
import pickle
import pandas as pd
import os

# -------------------------------
# PAGE CONFIG (MUST BE FIRST)
# -------------------------------
st.set_page_config(page_title="Churn Dashboard", layout="wide")

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

</style>
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
if st.button("🚀 Analyze Customer"):
    
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    # ---------------- RESULT ----------------
    if prediction == 1:
        st.markdown("⚠️ High Churn Risk")
    else:
        st.markdown("✅ Low Churn Risk")

    st.progress(float(probability))

    # ---------------- INSIGHTS ----------------
    st.markdown("### 📊 Key Insights")

    if probability > 0.7:
        st.warning("Customer likely to churn due to high charges or low tenure")
    elif probability > 0.4:
        st.info("Moderate risk — consider engagement offers")
    else:
        st.success("Customer is stable")

    # ---------------- GAUGE ----------------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        title={'text': "Churn Probability (%)"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    st.plotly_chart(fig)

    # ---------------- BAR CHART ----------------
    fig2 = go.Figure(data=[
        go.Bar(
            x=["Stay", "Churn"],
            y=[1 - probability, probability]
        )
    ])
    st.plotly_chart(fig2)
# -------------------------------
# INSIGHTS (OUTSIDE BUTTON)
# -------------------------------
st.markdown("### 💡 Key Insights")

st.markdown("""
<div class='card'>
<ul>
<li>High monthly charges increase churn risk</li>
<li>Low tenure customers are more likely to leave</li>
<li>Month-to-month contracts have highest churn</li>
</ul>
</div>
""", unsafe_allow_html=True)