import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Stroke Risk Prediction", page_icon="🧠")

st.title("🧠 Stroke Risk Prediction")
st.subheader("AI-powered stroke risk analysis using Machine Learning + LLM")

# --- Patient Input Form ---
st.header("Patient Information")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=1, max_value=100, value=37)
    hypertension = st.selectbox("Hypertension", ["Yes", "No"])
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])

with col2:
    work_type = st.selectbox("Work Type", ["Self-employed", "Private", "Govt job", "Never worked"])
    residence = st.selectbox("Residence Type", ["Urban", "Rural"])
    glucose = st.number_input("Avg Glucose Level", min_value=50, max_value=300, value=180)
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=32.0)
    smoking = st.selectbox("Smoking Status", ["Never smoked", "Formerly smoked", "Smokes", "Unknown"])

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
elif risk_score < 65:
    risk_level = "Medium"
else:
    risk_level = "High"

# --- Display Risk Score ---
st.header("Risk Result")

col3, col4, col5 = st.columns(3)
with col3:
    st.metric("Risk Score", f"{risk_score}%")
with col4:
    st.metric("Risk Level", risk_level)
with col5:
    st.metric("Probability", f"{risk_score/100:.2f}")

st.progress(risk_score / 100)

if risk_level == "Low":
    st.success(f"Low Risk — {risk_score}%")
elif risk_level == "Medium":
    st.warning(f"Medium Risk — {risk_score}%")
else:
    st.error(f"High Risk — {risk_score}%")

# --- LLM Explanation ---
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

Please provide:
1. Key risk factors for this patient
2. What contributes most to their risk
3. Actionable recommendations
4. Lifestyle changes they should consider

Be clear, concise, and avoid medical jargon."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

# --- Analyze Button ---
st.header("AI Explanation")

if st.button("🔍 Analyze with AI"):
    with st.spinner("Generating AI explanation..."):
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
        st.success("Analysis Complete!")
        st.write(explanation)

# --- Chat Interface ---
st.header("💬 Ask AI about the Results")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Ask anything about the patient's stroke risk..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    context = f"Patient: {age}yo {gender}, Hypertension:{hypertension}, Heart Disease:{heart_disease}, Glucose:{glucose}, BMI:{bmi}, Smoking:{smoking}. Risk: {risk_level} ({risk_score}%)"

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"You are a medical AI assistant analyzing stroke risk. Patient context: {context}. Answer concisely."},
                    *st.session_state.messages
                ],
                max_tokens=300
            )
            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
