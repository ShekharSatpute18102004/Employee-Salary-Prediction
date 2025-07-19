import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import random

# ===== Page Configuration =====
st.set_page_config(page_title="Salary Predictor 💼", page_icon="💸", layout="centered")

# ===== Custom CSS for Styling =====
st.markdown("""
<style>
    body {
        background-color: #f4f6f9;
    }
    .main {
        background: linear-gradient(145deg, #e0e0e0, #ffffff);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 1);
    }
    .css-1d391kg { background-color: #fff0;}
</style>
""", unsafe_allow_html=True)

# ===== Load Animation from URL =====
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie Animations
lottie_growth = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

# ===== Load Model =====
joblib.dump(model, 'rf_model.pkl')

# ===== Encodings =====
education_encoding = {"Enter Education": 0, "High School": 1, "Bachelor's": 2, "Master's": 3, "PhD": 4}
location_encoding = {"Enter Location": 0, "Rural": 1, "Suburban": 2, "Urban": 3}
job_title_encoding = {
    'Enter Job Title': 0, 'Clerk': 1, 'Customer Support': 2, 'Data Analyst': 3, 'Data Scientist': 4,
    'Director': 5, 'HR Manager': 6, 'Product Manager': 7, 'Software Engineer': 8, 'Technician': 9
}
gender_encoding = {'Male': 0, 'Female': 1}

# ===== Motivational Quotes =====
quotes = [
    "🚀 'The future depends on what you do today.' – Mahatma Gandhi",
    "🌟 'Success usually comes to those who are too busy to be looking for it.' – Henry David Thoreau",
    "💡 'Don’t watch the clock; do what it does. Keep going.' – Sam Levenson",
    "🔥 'Opportunities don't happen, you create them.' – Chris Grosser",
    "🎯 'Your career is your business. It’s time for you to manage it as a CEO.' – Dorit Sher"
]

# ===== Header Section =====
if lottie_growth:
    st_lottie(lottie_growth, height=200, key="ai")
st.title("💼 Employee Salary Prediction")
st.markdown("Enter employee details below to predict **realistic salary** based on market standards.")

# ===== Input Form Section =====
with st.form("input_form"):
    st.markdown("### 🔍 Enter Candidate Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        education = st.selectbox("🎓 Education", list(education_encoding.keys()))
        job_title = st.selectbox("💼 Job Title", list(job_title_encoding.keys()))
    with col2:
        experience = st.slider("👨‍💼 Experience (Years)", 0, 40, 2)
        gender = st.radio("🧍 Gender", list(gender_encoding.keys()), horizontal=True)
    with col3:
        location = st.selectbox("📍 Work Location", list(location_encoding.keys()))
        age = st.slider("🎂 Age", 18, 65, 24)

    growth_rate = st.slider("📈 Expected Annual Salary Growth Rate (%)", 0, 20, 7, help="Adjust the expected yearly salary increase rate for projection.")
    submitted = st.form_submit_button("🚀 Predict")

if submitted:
    missing_fields = []
    if education == "Enter Education":
        missing_fields.append("Education")
    if location == "Enter Location":
        missing_fields.append("Work Location")
    if job_title == "Enter Job Title":
        missing_fields.append("Job Title")

    if missing_fields:
        st.warning(f"⚠️ Please fill in the following fields before submitting: {', '.join(missing_fields)}")
    else:
        # Prepare features for prediction
        features = np.array([[
            education_encoding[education],
            experience,
            location_encoding[location],
            job_title_encoding[job_title],
            age,
            gender_encoding[gender]
        ]])
        df = pd.DataFrame(features, columns=['education_level', 'experience', 'location', 'job_title', 'age', 'gender'])

        # Predict Salary
        predicted_salary = model.predict(df)[0]

        # Color-coded salary range (example thresholds, adjust as needed)
        if predicted_salary < 30000:
            salary_color = "red"
            salary_msg = "Below average salary range"
        elif predicted_salary < 70000:
            salary_color = "orange"
            salary_msg = "Average salary range"
        else:
            salary_color = "green"
            salary_msg = "Above average salary range"

        st.markdown(f"### 💰 Estimated Monthly Salary: <span style='color:{salary_color};'>₹{predicted_salary:,.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"**{salary_msg}**")

        # ===== Salary Projection Chart =====
        st.markdown("### 📈 Career Growth Projection")
        years = np.arange(0, 11)
        projected_salaries = [predicted_salary * ((1 + growth_rate / 100) ** i) for i in years]

        fig = px.line(
            x=years,
            y=projected_salaries,
            markers=True,
            labels={'x': "Years from Now", 'y': "Projected Salary (INR)"}
        )
        fig.update_layout(title="10-Year Salary Projection", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # ===== Radar Chart: Profile Match =====
        st.markdown("### 🧭 Profile Match Radar Chart")

        ideal_profiles = {
            'Data Scientist': {'education_level': 3, 'experience': 5, 'age': 35},
            'Software Engineer': {'education_level': 2, 'experience': 4, 'age': 30},
            'Product Manager': {'education_level': 2, 'experience': 6, 'age': 35},
            'HR Manager': {'education_level': 2, 'experience': 7, 'age': 40},
            'Data Analyst': {'education_level': 2, 'experience': 3, 'age': 28},
            'Director': {'education_level': 3, 'experience': 15, 'age': 45},
            'Clerk': {'education_level': 1, 'experience': 2, 'age': 30},
            'Customer Support': {'education_level': 1, 'experience': 2, 'age': 28},
            'Technician': {'education_level': 1, 'experience': 3, 'age': 30}
        }

        ideal = ideal_profiles.get(job_title, {'education_level': 2, 'experience': 5, 'age': 30})

        categories = ['Education Level', 'Experience', 'Age']
        candidate_values = [
            education_encoding[education] / max(education_encoding.values()),
            experience / 40,
            age / 65
        ]
        ideal_values = [
            ideal['education_level'] / max(education_encoding.values()),
            ideal['experience'] / 40,
            ideal['age'] / 65
        ]

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=candidate_values,
            theta=categories,
            fill='toself',
            name='Your Profile',
            line_color='royalblue'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=ideal_values,
            theta=categories,
            fill='toself',
            name='Ideal Profile',
            line_color='orange'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title="Profile Match Radar"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # ===== Summary Card =====
        st.markdown("### 📝 Summary & Recommendations")
        summary = f"""
        - **Education Level:** {education}  
        - **Experience:** {experience} years  
        - **Age:** {age} years  
        - **Job Title:** {job_title}  
        - **Location:** {location}  
        - **Gender:** {gender}  

        Your predicted salary is ₹{predicted_salary:,.2f} with an expected growth rate of {growth_rate}%.  
        Compared to the ideal profile for a {job_title}, you are {'well aligned' if all(cv >= iv for cv, iv in zip(candidate_values, ideal_values)) else 'encouraged to improve in some areas'}.
        """

        st.info(summary)

        # ===== Career Tips =====
        st.markdown("### 🎯 Career Advice & Tips")
        tips = {
            'Clerk': "📚 Learn spreadsheet tools like Excel and automation basics.<br>🧠 Improve time management and digital record handling.",
            'Customer Support': "🎧 Master CRM tools like Salesforce.<br>📞 Sharpen your empathy and conflict resolution skills.",
            'Data Analyst': "📊 Master SQL, Python, and Tableau/Power BI.<br>📈 Turn raw data into actionable business insights.",
            'Data Scientist': "🤖 Practice machine learning & deep learning.<br>📚 Participate in Kaggle, learn PyTorch & Big Data tools.",
            'Director': "🏗️ Lead with strategic thinking and vision.<br>📈 Learn stakeholder management and business transformation.",
            'HR Manager': "💼 Strengthen HR analytics and labor law knowledge.<br>🧠 Upskill in employee engagement & DEI practices.",
            'Product Manager': "🧪 Learn agile, SCRUM, and user-centric design.<br>📊 Blend business acumen with data-driven decisions.",
            'Software Engineer': "💻 Sharpen coding, DSA, and system design.<br>🌐 Master DevOps, scalable systems, and cloud tech.",
            'Technician': "🛠️ Learn diagnostics and automation tools.<br>⚙️ Certify in hardware, networking, or cloud services."
        }

        if job_title in tips:
            st.markdown(f"""
            <div style='
                background-color:  #1b3251ff;
                padding: 15px;
                border-radius: 10px;
                font-size: 16px;
                line-height: 1.6;
                color: white;
            '>
                {tips[job_title]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("🚀 Keep building your expertise and networking in your domain!")

        # ===== Motivational Quote =====
        st.markdown("### 💡 Motivational Quote")
        st.success(random.choice(quotes))

        
# ===== Footer =====
st.markdown("""
<hr>
<div style="text-align:center">
    <strong>Made with ❤️ by Shekhar Satpute </strong><br>
          AI Salary Predictor App
            License: MIT License 
            (c) 2025 Shekhar Satpute
</div>
""", unsafe_allow_html=True)

