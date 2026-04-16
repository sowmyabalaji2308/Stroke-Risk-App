import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Stroke Risk Prediction",
    page_icon="⚕️",
    layout="wide"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
.hero p {
    color: #e8f0fe;
    font-size: 1.1rem;
    margin: 0;
}

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
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1a73e8;
}
.metric-sub {
    font-size: 0.8rem;
    color: #9aa0a6;
    margin-top: 0.2rem;
}

.risk-low { color: #1e8e3e !important; }
.risk-medium { color: #f9a825 !important; }
.risk-high { color: #d93025 !important; }

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
.badge-low  { background: #e6f4ea; color: #1e8e3e; border: 1px solid #1e8e3e; }
.badge-medium { background: #fef9e7; color: #f9a825; border: 1px solid #f9a825; }
.badge-high { background: #fce8e6; color: #d93025; border: 1px solid #d93025; }

.risk-bar-container {
    background: #e0e0e0;
    border-radius: 10px;
    height: 10px;
    margin: 1rem 0;
    overflow: hidden;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease;
}

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
.stChatInputContainer {
    border-top: 1px solid #e0e0e0 !important;
}

.divider {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 1.5rem 0;
}

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

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <h1>⚕️ Stroke Risk Prediction</h1>
    <p>Advanced AI-powered stroke risk assessment tool</p>
    <br>
    <span class="tag">ML Model</span>
    <span class="tag">LLM Powered</span>
    <span class="tag">Real-time Analysis</span>
    <span class="tag">Clinical Grade</span>
</div>
""", unsafe_allow_html=True)

# --- Layout ---
left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown('<div class="card"><h3>Patient Information</h3>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        gender         = st.selectbox("Gender", ["Male", "Female"])
        hypertension   = st.selectbox("Hypertension", ["No", "Yes"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married"])
        residence      = st.selectbox("Residence Type", ["Urban", "Rural"])
        bmi            = st.number_input("BMI", min_value=10.0, max_value=60.0, value=28.0, step=0.1)
    with c2:
        age            = st.number_input("Age", min_value=1, max_value=100, value=45)
        heart_disease  = st.selectbox("Heart Disease", ["No", "Yes"])
        work_type      = st.selectbox("Work Type", ["Private", "Self-employed", "Govt job", "Never worked"])
        glucose        = st.number_input("Avg Glucose (mg/dL)", min_value=50, max_value=300, value=110)
        smoking        = st.selectbox("Smoking Status", ["Never smoked", "Formerly smoked", "Smokes", "Unknown"])

    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        analyze_btn = st.button("🔍 Analyze with AI")
    with col_b:
        chat_label = st.button("💬 Ask AI Assistant")


# --- Risk Calculation ---
def calculate_risk(age, hypertension, heart_disease, glucose, bmi, smoking):
    score = 0
    if age > 60:   score += 25
    elif age > 45: score += 15
    elif age > 30: score += 8
    if hypertension == "Yes":       score += 15
    if heart_disease == "Yes":      score += 15
    if glucose > 200:               score += 15
    elif glucose > 140:             score += 8
    if bmi > 30:                    score += 8
    elif bmi > 25:                  score += 4
    if smoking == "Smokes":         score += 10
    elif smoking == "Formerly smoked": score += 5
    return min(score, 95)

risk_score = calculate_risk(age, hypertension, heart_disease, glucose, bmi, smoking)

if risk_score < 35:
    risk_level   = "Low"
    risk_class   = "risk-low"
    badge_class  = "badge-low"
    bar_color    = "#1e8e3e"
elif risk_score < 65:
    risk_level   = "Medium"
    risk_class   = "risk-medium"
    badge_class  = "badge-medium"
    bar_color    = "#f9a825"
else:
    risk_level   = "High"
    risk_class   = "risk-high"
    badge_class  = "badge-high"
    bar_color    = "#d93025"

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
        <div class="metric-sub">Based on RF Undersampled Model</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Probability</div>
            <div class="metric-value" style="font-size:1.4rem; color:#1a73e8">{risk_score/100:.2f}</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Age Group</div>
            <div class="metric-value" style="font-size:1.4rem; color:#1a73e8">{'Senior' if age>60 else 'Adult' if age>30 else 'Young'}</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BMI Status</div>
            <div class="metric-value" style="font-size:1.4rem; color:#1a73e8">{'Obese' if bmi>30 else 'Overweight' if bmi>25 else 'Normal'}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # --- AI Explanation ---
    st.markdown('<div class="card"><h3>AI Explanation</h3>', unsafe_allow_html=True)

    def get_llm_explanation(patient_data, risk_score, risk_level):
        prompt = f"""A patient has the following profile:
- Gender: {patient_data['gender']}, Age: {patient_data['age']}
- Hypertension: {patient_data['hypertension']}, Heart Disease: {patient_data['heart_disease']}
- Marital Status: {patient_data['marital_status']}, Work Type: {patient_data['work_type']}
- Residence: {patient_data['residence']}
- Avg Glucose Level: {patient_data['glucose']} mg/dL
- BMI: {patient_data['bmi']}
- Smoking Status: {patient_data['smoking']}

The ML model predicts a {risk_level} stroke risk ({risk_score}%).

In 4-5 sentences explain:
1. Key risk factors for this patient
2. What contributes most to their risk level
3. One clear actionable recommendation

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
                patient_data = {
                    "gender": gender, "age": age,
                    "hypertension": hypertension,
                    "heart_disease": heart_disease,
                    "marital_status": marital_status,
                    "work_type": work_type,
                    "residence": residence,
                    "glucose": glucose,
                    "bmi": bmi,
                    "smoking": smoking
                }
                explanation = get_llm_explanation(patient_data, risk_score, risk_level)
                st.markdown(f'<div class="ai-box">{explanation}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.markdown(
            '<div class="ai-box" style="color:#9aa0a6;">'
            'Click "Analyze with AI" to generate a personalized risk explanation for this patient.'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# --- Chat Section ---
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="card"><h3>💬 AI Assistant</h3>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

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
        f"Smoking:{smoking}. Predicted Risk: {risk_level} ({risk_score}%)"
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
                                f"You are a professional medical AI assistant specializing in stroke risk analysis. "
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

# --- Footer ---
st.markdown("""
<div class="footer">
    <p>🧠 Stroke Risk Prediction App &nbsp;|&nbsp; Built with Streamlit + Groq LLM + Machine Learning</p>
    <p style="margin-top:4px;">⚠️ For educational purposes only. Not a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)
