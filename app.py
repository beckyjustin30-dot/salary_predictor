# app.py
# Salary Prediction System - Dark Blue and Green Theme

import streamlit as st
import pickle
import os
from model import train_model, predict_salary, get_options

st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
    <style>
        .stApp { background-color: #020b18; }

        .header {
            background-color: #041c2c;
            border-bottom: 2px solid #00a86b;
            padding: 20px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-radius: 14px;
            margin-bottom: 25px;
        }
        .header-logo { font-size: 36px; font-weight: bold; color: #00a86b; font-family: Arial; }
        .header-logo span { color: #4fc3f7; }
        .header-tagline { color: #90e0ef; font-size: 14px; }
        .header-badge { background-color: #020b18; color: #4fc3f7; border: 1px solid #4fc3f7; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: bold; }

        .section-header-green { color: #00a86b; font-size: 15px; font-weight: bold; border-bottom: 2px solid #00a86b; padding-bottom: 6px; margin-bottom: 12px; }
        .section-header-blue { color: #4fc3f7; font-size: 15px; font-weight: bold; border-bottom: 2px solid #4fc3f7; padding-bottom: 6px; margin-bottom: 12px; }

        .panel-green { background-color: #041c2c; border: 1px solid #00a86b; padding: 20px; border-radius: 14px; margin-bottom: 15px; }
        .panel-blue { background-color: #041c2c; border: 1px solid #4fc3f7; padding: 20px; border-radius: 14px; margin-bottom: 15px; }

        .salary-box {
            background-color: #020b18;
            color: #00a86b;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            border: 2px solid #00a86b;
            margin-bottom: 15px;
        }
        .salary-label { color: #90e0ef; font-size: 14px; margin-bottom: 5px; }

        .metric-box {
            background-color: #020b18;
            border: 1px solid #00a86b;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }
        .metric-label { color: #90e0ef; font-size: 12px; margin-bottom: 4px; }
        .metric-value { color: #00a86b; font-size: 20px; font-weight: bold; }

        .tip-box { background-color: #041c2c; border-left: 4px solid #00a86b; border-radius: 8px; padding: 15px; color: #90e0ef; font-size: 13px; line-height: 1.8; }

        .model-badge { display: inline-block; background-color: #020b18; color: #4fc3f7; border: 1px solid #4fc3f7; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin: 3px; }
        .model-badge-green { display: inline-block; background-color: #020b18; color: #00a86b; border: 1px solid #00a86b; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin: 3px; }

        .footer { background-color: #041c2c; border-top: 2px solid #00a86b; padding: 20px 40px; border-radius: 14px; margin-top: 30px; text-align: center; }
        .footer-title { color: #00a86b; font-size: 18px; font-weight: bold; margin-bottom: 6px; }
        .footer-text { color: #90e0ef; font-size: 13px; margin-bottom: 4px; }
        .footer-badge { display: inline-block; background-color: #020b18; color: #00a86b; border: 1px solid #00a86b; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin: 3px; }

        .stButton > button { background-color: #041c2c; color: #ffffff; border: 2px solid #00a86b; padding: 12px 40px; border-radius: 25px; font-size: 17px; font-weight: bold; width: 100%; }
        .stButton > button:hover { background-color: #00a86b; color: #020b18; }
        .stSelectbox label { color: #90e0ef !important; }
        .stSlider label { color: #90e0ef !important; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("""
    <div class="header">
        <div>
            <div class="header-logo">💰 SalaryIQ <span>🧠</span></div>
            <div class="header-tagline">AI powered salary prediction — know your worth instantly!</div>
        </div>
        <div class="header-badge">🤖 Powered by Machine Learning</div>
    </div>
""", unsafe_allow_html=True)

# Train model if not already trained
if not os.path.exists('model.pkl'):
    with st.spinner("🤖 Training AI model for the first time... Please wait!"):
        scores = train_model()
    st.success("✅ AI Model trained successfully!")
else:
    scores = None

# Get options
options = get_options()

# ===== BODY =====
st.markdown('<div class="panel-green">', unsafe_allow_html=True)
st.markdown('<p class="section-header-green">📋 Enter Your Professional Details</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    job_title = st.selectbox("🏢 Job Title", options['job_titles'])
    education = st.selectbox("🎓 Education Level", options['education'])

with col2:
    experience = st.slider("📅 Years of Experience", 0, 25, 3)
    industry = st.selectbox("🏭 Industry", options['industries'])

with col3:
    location = st.selectbox("📍 Location", options['locations'])
    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("💰 Predict My Salary")

st.markdown('</div>', unsafe_allow_html=True)

# ===== PREDICTION =====
if predict_btn:
    with st.spinner("🤖 Calculating your expected salary..."):
        salary = predict_salary(job_title, education, experience, industry, location)

    st.markdown("---")

    # Save to session
    st.session_state.salary = salary
    st.session_state.job_title = job_title
    st.session_state.education = education
    st.session_state.experience = experience
    st.session_state.industry = industry
    st.session_state.location = location
    st.session_state.predicted = True

    # Salary display
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="panel-green">', unsafe_allow_html=True)
        st.markdown('<p class="section-header-green">💰 Your Predicted Salary</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="salary-label">Expected Monthly Salary (RWF)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="salary-box">{salary:,.0f} RWF</div>', unsafe_allow_html=True)

        # Annual salary
        annual = salary * 12
        st.markdown(f'<div class="salary-label">Expected Annual Salary</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#4fc3f7; font-size:22px; font-weight:bold; text-align:center; margin-bottom:15px;">{annual:,.0f} RWF / year</div>', unsafe_allow_html=True)

        # Min and Max range
        min_sal = round(salary * 0.85, -3)
        max_sal = round(salary * 1.15, -3)
        st.markdown(f'<div class="salary-label">Salary Range</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#90e0ef; text-align:center; font-size:15px;">{min_sal:,.0f} — {max_sal:,.0f} RWF</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="panel-blue">', unsafe_allow_html=True)
        st.markdown('<p class="section-header-blue">📊 Your Profile Summary</p>', unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f'<div class="metric-box"><div class="metric-label">Job Title</div><div class="metric-value" style="font-size:14px;">{job_title}</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box"><div class="metric-label">Education</div><div class="metric-value" style="font-size:14px;">{education}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><div class="metric-label">Experience</div><div class="metric-value">{experience} yrs</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="metric-box"><div class="metric-label">Location</div><div class="metric-value" style="font-size:14px;">{location}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box"><div class="metric-label">Industry</div><div class="metric-value" style="font-size:14px;">{industry}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Career tips
    st.markdown('<div class="panel-green">', unsafe_allow_html=True)
    st.markdown('<p class="section-header-green">💡 Career Tips to Boost Your Salary</p>', unsafe_allow_html=True)

    tips = []
    if education == "High School":
        tips.append("🎓 Consider pursuing a Bachelor's degree to increase your earning potential by up to 40%.")
    elif education == "Bachelor":
        tips.append("🎓 A Master's degree could increase your salary by 20-30% in your field.")
    if experience < 3:
        tips.append("📅 Build more experience through internships and projects — each year adds significant value.")
    if experience >= 5:
        tips.append("⭐ With your experience level, consider applying for senior or team lead positions.")
    if location != "Kigali":
        tips.append("📍 Salaries in Kigali are typically 20% higher — consider remote work opportunities.")
    tips.append("📜 Earn relevant certifications to stand out and command higher salaries.")
    tips.append("🤝 Build your professional network — many high-paying jobs are filled through referrals.")

    for tip in tips[:4]:
        st.markdown(f'<div class="tip-box" style="margin-bottom:8px;">{tip}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Model accuracy
    st.markdown('<div class="panel-blue">', unsafe_allow_html=True)
    st.markdown('<p class="section-header-blue">📈 Model Performance</p>', unsafe_allow_html=True)
    st.write("Our AI uses Random Forest — the most accurate model:")

    try:
        with open('model.pkl', 'rb') as f:
            model, encoders = pickle.load(f)
        st.markdown('<span class="model-badge-green">✅ Random Forest — Best Model</span>', unsafe_allow_html=True)
        st.markdown('<span class="model-badge">📊 Linear Regression — Compared</span>', unsafe_allow_html=True)
        st.markdown('<span class="model-badge">🌳 Decision Tree — Compared</span>', unsafe_allow_html=True)
    except:
        pass
    st.markdown('</div>', unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""
    <div class="footer">
        <div class="footer-title">💰 SalaryIQ 🧠</div>
        <div class="footer-text">AI powered salary prediction built with Python and Machine Learning</div>
        <div class="footer-text" style="margin-top: 10px;">
            <span class="footer-badge">🤖 Random Forest</span>
            <span class="footer-badge">🐍 Python</span>
            <span class="footer-badge">📊 Scikit-learn</span>
            <span class="footer-badge">🌿 Streamlit</span>
        </div>
        <div class="footer-text" style="margin-top: 10px; color: #00a86b;">
            © 2026 SalaryIQ — Built by Becky 💚
        </div>
    </div>
""", unsafe_allow_html=True)