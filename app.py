import streamlit as st
import pickle
import pandas as pd
import numpy as np
from groq import Groq

st.set_page_config(
    page_title="Stroke Risk Prediction",
    page_icon="⚕️",
    layout="wide"
)

# ── Load model and feature columns ──────────────────────────────────
@st.cache_resource
def load_model():
    with open("stroke_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

@st.cache_resource
def load_features():
    with open("feature_cols.pkl", "rb") as f:
        feature_cols = pickle.load(f)
    return feature_cols

model = load_model()
feature_cols = load_features()

# ── Groq LLM client ─────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ── Light theme CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: #f0f4f8;
    color: #1a1a2e;
}

section[data-testid="stSidebar"] { display: none; }

.hero {
    background: linear-gradient(135deg, #1a73e8 0%, #1557b0 50%, #0d47a1 100%);
    border-radius: 20px;
    padding: 3rem;
    margin-bottom: 2rem;
    border: 1px solid #1a73e8;
    box-shadow: 0 4px 20px rgba(26,115,232,0.2);
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    -webkit-text-fill-color: #ffffff;
    margin-bottom: 0.5rem;
}
.hero p { color: #e8f0fe; font-size: 1.1rem; margin: 0; }

.card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.card h3 {
    color: #1a73e8;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 0.8rem;
}

.metric-card {
    background: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.metric-label {
    color: #5f6368;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.4rem;
}
.metric-value { font-size: 2.2rem; font-weight: 700; color: #1a73e8; }
.metric-sub { font-size: 0.8rem; color: #9aa0a6; margin-top: 0.2rem; }

.risk-low    { color: #1e8e3e !important; }
.risk-medium { color: #f9a825 !important; }
.risk-high   { color: #d93025 !important; }

.badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.badge-low    { background: #e6f4ea; color: #1e8e3e; border: 1px solid #1e8e3e; }
.badge-medium { background: #fef9e7; color: #f9a825; border: 1px solid #f9a825; }
.badge-high   { background: #fce8e6; color: #d93025; border: 1px solid #d93025; }

.risk-bar-container {
    background: #e0e0e0;
    border-radius: 10px;
    height: 10px;
    margin: 1rem 0;
    overflow: hidden;
}
.risk-bar-fill { height: 100%; border-radius: 10px; transition: width 0.5s ease; }

.ai-box {
    background: #e8f0fe;
    border: 1px solid #c5d8fb;
    border-radius: 12px;
    padding: 1.2rem;
    color: #1a1a2e;
    font-size: 0.92rem;
    line-height: 1.8;
    margin-top: 1rem;
}

.stButton > button {
    background: linear-gradient(135deg, #1a73e8, #1557b0) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 15px rgba(26,115,232,0.3) !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(26,115,232,0.5) !important;
    transform: translateY(-1px) !important;
}

.stSelectbox > div > div {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    color: #1a1a2e !important;
}
.stNumberInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    color: #1a1a2e !important;
}

label {
    color: #5f6368 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

.stChatMessage {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem !important;
}
.stChatInputContainer { border-top: 1px solid #e0e0e0 !important; }

.divider { border: none; border-top: 1px solid #e0e0e0; margin: 1.5rem 0; }

.tag {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
    letter-spacing: 0.5px;
}

.footer {
    text-align: center;
    color: #9aa0a6;
    font-size: 0.8rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid #e0e0e0;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>⚕️ Stroke Risk Prediction</h1>
    <p>Advanced AI-powered stroke risk assessment tool</p>
    <br>
    <span class="tag">XGBoost Model</span>
    <span class="tag">LLM Powered</span>
    <span class="tag">Real-time Analysis</span>
    <span class="tag">Clinical Grade</span>
</div>
""", unsafe_allow_html=True)

# ── Patient inputs ────────────────────────────────────────────────────
left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown('<div class="card"><h3>Patient Information</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        gender         = st.selectbox("Gender",         ["Female", "Male"])
        hypertension   = st.selectbox("Hypertension",   ["No", "Yes"])
        marital_status = st.selectbox("Ever Married",   ["No", "Yes"])
        residence      = st.selectbox("Residence Type", ["Rural", "Urban"])
        bmi            = st.number_input("BMI", min_value=10.0, max_value=97.0, value=28.0, step=0.1)
    with c2:
        age            = st.number_input("Age", min_value=1, max_value=100, value=45)
        heart_disease  = st.selectbox("Heart Disease",  ["No", "Yes"])
        work_type      = st.selectbox("Work Type",      ["Govt_job", "Never_worked", "Private", "Self-employed", "children"])
        glucose        = st.number_input("Avg Glucose (mg/dL)", min_value=50.0, max_value=300.0, value=110.0)
        smoking        = st.selectbox("Smoking Status", ["Unknown", "formerly smoked", "never smoked", "smokes"])
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        analyze_btn = st.button("🔍 Analyze with AI")
    with col_b:
        reset_btn = st.button("🔄 Reset Chat")


# ── Build model input ─────────────────────────────────────────────────
def build_input():
    """
    Replicate the exact one-hot encoding your Colab notebook produced
    via pd.get_dummies(..., drop_first=True) on the stroke dataset.
    Reference (dropped) categories:
      gender        → Female
      ever_married  → No
      work_type     → Govt_job
      Residence     → Rural
      smoking       → Unknown
    """
    row = {
        "age":               age,
        "hypertension":      1 if hypertension == "Yes" else 0,
        "heart_disease":     1 if heart_disease == "Yes" else 0,
        "avg_glucose_level": glucose,
        "bmi":               bmi,
        # gender
        "gender_Male":              1 if gender == "Male"          else 0,
        "gender_Other":             1 if gender == "Other"         else 0,
        # ever_married
        "ever_married_Yes":         1 if marital_status == "Yes"   else 0,
        # work_type
        "work_type_Never_worked":   1 if work_type == "Never_worked"  else 0,
        "work_type_Private":        1 if work_type == "Private"       else 0,
        "work_type_Self-employed":  1 if work_type == "Self-employed" else 0,
        "work_type_children":       1 if work_type == "children"      else 0,
        # Residence_type
        "Residence_type_Urban":     1 if residence == "Urban"      else 0,
        # smoking_status
        "smoking_status_formerly smoked": 1 if smoking == "formerly smoked" else 0,
        "smoking_status_never smoked":    1 if smoking == "never smoked"    else 0,
        "smoking_status_smokes":          1 if smoking == "smokes"          else 0,
    }
    df = pd.DataFrame([row])
    # Align to exact training column order — fills any missing with 0
    df = df.reindex(columns=feature_cols, fill_value=0)
    return df


def predict_stroke():
    input_df = build_input()
    prob = model.predict_proba(input_df)[0][1]
    return round(prob * 100, 1)


risk_score = predict_stroke()

if risk_score < 35:
    risk_level  = "Low"
    risk_class  = "risk-low"
    badge_class = "badge-low"
    bar_color   = "#1e8e3e"
elif risk_score < 65:
    risk_level  = "Medium"
    risk_class  = "risk-medium"
    badge_class = "badge-medium"
    bar_color   = "#f9a825"
else:
    risk_level  = "High"
    risk_class  = "risk-high"
    badge_class = "badge-high"
    bar_color   = "#d93025"

# ── Right column ──────────────────────────────────────────────────────
with right:
    st.markdown('<div class="card"><h3>Risk Assessment</h3>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Stroke Risk Score</div>
        <div class="metric-value {risk_class}">{risk_score}%</div>
        <div class="risk-bar-container">
            <div class="risk-bar-fill" style="width:{risk_score}%; background:{bar_color};"></div>
        </div>
        <span class="badge {badge_class}">{risk_level} Risk</span>
        <div class="metric-sub">XGBoost Undersampled Model · 92% Sensitivity</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Probability</div>
            <div class="metric-value" style="font-size:1.4rem;color:#1a73e8">{risk_score/100:.2f}</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        age_group = "Senior" if age > 60 else "Adult" if age > 30 else "Young"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Age Group</div>
            <div class="metric-value" style="font-size:1.4rem;color:#1a73e8">{age_group}</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        bmi_status = "Obese" if bmi > 30 else "Overweight" if bmi > 25 else "Normal"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BMI Status</div>
            <div class="metric-value" style="font-size:1.4rem;color:#1a73e8">{bmi_status}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── AI Explanation ───────────────────────────────────────────────
    st.markdown('<div class="card"><h3>AI Explanation</h3>', unsafe_allow_html=True)

    def get_llm_explanation():
        prompt = f"""A patient has the following profile:
- Gender: {gender}, Age: {age}
- Hypertension: {hypertension}, Heart Disease: {heart_disease}
- Ever Married: {marital_status}, Work Type: {work_type}
- Residence: {residence}
- Avg Glucose Level: {glucose} mg/dL
- BMI: {bmi}
- Smoking Status: {smoking}

The XGBoost ML model (92% sensitivity) predicts a {risk_level} stroke risk of {risk_score}%.

In 4-5 sentences:
1. Explain the key risk factors driving this prediction
2. What contributes most to their risk level
3. Give one clear actionable recommendation

Be concise, professional, and avoid medical jargon."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return response.choices[0].message.content

    if analyze_btn:
        with st.spinner("Analyzing patient profile..."):
            try:
                explanation = get_llm_explanation()
                st.markdown(f'<div class="ai-box">{explanation}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.markdown(
            '<div class="ai-box" style="color:#9aa0a6;">'
            'Click "Analyze with AI" to generate a personalised risk explanation for this patient.'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ── Chat Section ──────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="card"><h3>💬 AI Assistant</h3>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_btn:
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Ask anything about stroke risk, prevention, or this patient..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    context = (
        f"Patient: {age}yo {gender}, Hypertension:{hypertension}, "
        f"Heart Disease:{heart_disease}, Glucose:{glucose}, BMI:{bmi}, "
        f"Smoking:{smoking}. XGBoost predicted: {risk_level} risk ({risk_score}%)"
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"You are a professional medical AI assistant specialising in stroke risk. "
                                f"Patient context: {context}. Be concise, clear, and professional."
                            )
                        },
                        *st.session_state.messages
                    ],
                    max_tokens=300
                )
                reply = response.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p>🧠 Stroke Risk Prediction App &nbsp;|&nbsp; Built with Streamlit + Groq LLM + XGBoost</p>
    <p style="margin-top:4px;">⚠️ For educational purposes only. Not a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)
