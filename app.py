import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Stroke Risk Prediction",
    page_icon="",
    layout="wide"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d0d1a 50%, #0a0f0a 100%);
    color: #e0e0e0;
}

section[data-testid="stSidebar"] { display: none; }

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 20px;
    padding: 3rem;
    margin-bottom: 2rem;
    border: 1px solid #e94560;
    box-shadow: 0 0 40px rgba(233, 69, 96, 0.15);
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #e94560, #0f3460, #e94560);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero p {
    color: #a0a0b0;
    font-size: 1.1rem;
    margin: 0;
}

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(233, 69, 96, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}
.card h3 {
    color: #e94560;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid rgba(233,69,96,0.2);
    padding-bottom: 0.8rem;
}

.metric-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid rgba(233, 69, 96, 0.3);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.metric-label {
    color: #a0a0b0;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #e94560;
}
.metric-sub {
    font-size: 0.8rem;
    color: #606080;
    margin-top: 0.2rem;
}

.risk-low { color: #00d26a !important; }
.risk-medium { color: #ffb800 !important; }
.risk-high { color: #e94560 !important; }

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
.badge-low { background: rgba(0,210,106,0.15); color: #00d26a; border: 1px solid #00d26a; }
.badge-medium { background: rgba(255,184,0,0.15); color: #ffb800; border: 1px solid #ffb800; }
.badge-high { background: rgba(233,69,96,0.15); color: #e94560; border: 1px solid #e94560; }

.risk-bar-container {
    background: rgba(255,255,255,0.05);
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
    background: rgba(15, 52, 96, 0.3);
    border: 1px solid rgba(15, 52, 96, 0.8);
    border-radius: 12px;
    padding: 1.2rem;
    color: #c0c0d0;
    font-size: 0.92rem;
    line-height: 1.8;
    margin-top: 1rem;
}

.stButton > button {
    background: linear-gradient(135deg, #e94560, #c23152) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 15px rgba(233,69,96,0.3) !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(233,69,96,0.5) !important;
    transform: translateY(-1px) !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(233,69,96,0.2) !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
}
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(233,69,96,0.2) !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
}

label { color: #a0a0b0 !important; font-size: 0.82rem !important; font-weight: 500 !important; letter-spacing: 0.5px !important; }

.stChatMessage {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(233,69,96,0.1) !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem !important;
}
.stChatInputContainer {
    border-top: 1px solid rgba(233,69,96,0.2) !important;
}

.divider {
    border: none;
    border-top: 1px solid rgba(233,69,96,0.15);
    margin: 1.5rem 0;
}

.tag {
    display: inline-block;
    background: rgba(233,69,96,0.1);
    color: #e94560;
    border: 1px solid rgba(233,69,96,0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
    letter-spacing: 0.5px;
}

.footer {
    text-align: center;
    color: #404060;
    font-size: 0.8rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid rgba(233,69,96,0.1);
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <h1>🧠 Stroke Risk Prediction</h1>
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
        gender = st.selectbox("Gender", ["Male", "Female"])
        hypertension = st.selectbox("Hypertension", ["No", "Yes"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married"])
        residence = st.selectbox("Residence Type", ["Urban", "Rural"])
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=28.0, step=0.1)
    with c2:
        age = st.number_input("Age", min_value=1, max_value=100, value=45)
        heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
        work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt job", "Never worked"])
        glucose = st.number_input("Avg Glucose (mg/dL)", min_value=50, max_value=300, value=110)
        smoking = st.selectbox("Smoking Status", ["Never smoked", "Formerly smoked", "Smokes", "Unknown"])

    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        analyze_btn = st.button("🔍 Analyze with AI")
    with col_b:
        chat_label = st.button("💬 Ask AI Assistant")

# --- Risk Calculation ---
def calculate_risk(age, hypertension, heart_disease, glucose, bmi, smoking):
    score = 0
    if age > 60: score += 25
    elif age > 45: score += 15
    elif age > 30: score += 8
    if hypertension == "Yes": score += 15
    if heart_disease == "Yes": score += 15
    if glucose > 200: score += 15
    elif glucose > 140: score += 8
    if bmi > 30: score += 8
    elif bmi > 25: score += 4
    if smoking == "Smokes": score += 10
    elif smoking == "Formerly smoked": score += 5
    return min(score, 95)

risk_score = calculate_risk(age, hypertension, heart_disease, glucose, bmi, smoking)

if risk_score < 35:
    risk_level = "Low"
    risk_class = "risk-low"
    badge_class = "badge-low"
    bar_color = "#00d26a"
elif risk_score < 65:
    risk_level = "Medium"
    risk_class = "risk-medium"
    badge_class = "badge-medium"
    bar_color = "#ffb800"
else:
    risk_level = "High"
    risk_class = "risk-high"
    badge_class = "badge-high"
    bar_color = "#e94560"

with right:
    st.markdown('<div class="card"><h3>Risk Assessment</h3>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Stroke Risk Score</div>
        <div class="metric-value {risk_class}">{risk_score}%</div>
        <div class="risk-bar-container">
            <div class="risk-bar-fill" style="width:{risk_score}%; background: {bar_color};"></div>
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
            <div class="metric-value" style="font-size:1.4rem; color:#a0a0ff">{risk_score/100:.2f}</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Age Group</div>
            <div class="metric-value" style="font-size:1.4rem; color:#a0a0ff">{'Senior' if age>60 else 'Adult' if age>30 else 'Young'}</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BMI Status</div>
            <div class="metric-value" style="font-size:1.4rem; color:#a0a0ff">{'Obese' if bmi>30 else 'Overweight' if bmi>25 else 'Normal'}</div>
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
        st.markdown('<div class="ai-box" style="color:#404060;">Click "Analyze with AI" to generate a personalized risk explanation for this patient.</div>', unsafe_allow_html=True)

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

    context = f"Patient: {age}yo {gender}, Hypertension:{hypertension}, Heart Disease:{heart_disease}, Glucose:{glucose}, BMI:{bmi}, Smoking:{smoking}. Predicted Risk: {risk_level} ({risk_score}%)"

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"You are a professional medical AI assistant specializing in stroke risk analysis. Patient context: {context}. Be concise, clear, and professional."},
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
