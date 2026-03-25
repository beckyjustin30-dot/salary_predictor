# model.py
# Salary Prediction System - ML Model

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
import pickle

def create_dataset():
    np.random.seed(42)
    n = 1000

    job_titles = ['Software Engineer', 'Data Analyst', 'Project Manager',
                  'IT Officer', 'System Administrator', 'Data Scientist',
                  'Web Developer', 'Network Engineer', 'Database Administrator',
                  'Business Analyst']

    education = ['High School', 'Bachelor', 'Master', 'PhD']
    industries = ['Technology', 'Finance', 'Healthcare', 'Education',
                  'Government', 'NGO', 'Telecommunications', 'Banking']
    locations = ['Kigali', 'Huye', 'Musanze', 'Rubavu', 'Nyagatare', 'Remote']
    experience = np.random.randint(0, 25, n)

    job_title_list = np.random.choice(job_titles, n)
    education_list = np.random.choice(education, n)
    industry_list = np.random.choice(industries, n)
    location_list = np.random.choice(locations, n)

    base_salary = {
        'Software Engineer': 800000,
        'Data Scientist': 950000,
        'Project Manager': 900000,
        'Data Analyst': 750000,
        'IT Officer': 600000,
        'System Administrator': 650000,
        'Web Developer': 700000,
        'Network Engineer': 680000,
        'Database Administrator': 720000,
        'Business Analyst': 780000
    }

    edu_multiplier = {
        'High School': 0.7,
        'Bachelor': 1.0,
        'Master': 1.3,
        'PhD': 1.6
    }

    loc_multiplier = {
        'Kigali': 1.2,
        'Remote': 1.1,
        'Rubavu': 1.0,
        'Musanze': 0.95,
        'Huye': 0.9,
        'Nyagatare': 0.85
    }

    salaries = []
    for i in range(n):
        base = base_salary[job_title_list[i]]
        edu = edu_multiplier[education_list[i]]
        loc = loc_multiplier[location_list[i]]
        exp_bonus = experience[i] * 25000
        noise = np.random.normal(0, 50000)
        salary = (base * edu * loc) + exp_bonus + noise
        salary = max(200000, salary)
        salaries.append(round(salary, -3))

    df = pd.DataFrame({
        'job_title': job_title_list,
        'education': education_list,
        'experience_years': experience,
        'industry': industry_list,
        'location': location_list,
        'salary': salaries
    })
    return df

def train_model():
    df = create_dataset()

    le_job = LabelEncoder()
    le_edu = LabelEncoder()
    le_ind = LabelEncoder()
    le_loc = LabelEncoder()

    df['job_encoded'] = le_job.fit_transform(df['job_title'])
    df['edu_encoded'] = le_edu.fit_transform(df['education'])
    df['ind_encoded'] = le_ind.fit_transform(df['industry'])
    df['loc_encoded'] = le_loc.fit_transform(df['location'])

    X = df[['job_encoded', 'edu_encoded', 'experience_years', 'ind_encoded', 'loc_encoded']]
    y = df['salary']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_score = r2_score(y_test, rf.predict(X_test))

    # Train Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_score = r2_score(y_test, lr.predict(X_test))

    # Train Decision Tree
    dt = DecisionTreeRegressor(random_state=42)
    dt.fit(X_train, y_train)
    dt_score = r2_score(y_test, dt.predict(X_test))

    encoders = {
        'job': le_job,
        'edu': le_edu,
        'ind': le_ind,
        'loc': le_loc
    }

    scores = {
        'Random Forest': round(rf_score * 100, 2),
        'Linear Regression': round(lr_score * 100, 2),
        'Decision Tree': round(dt_score * 100, 2)
    }

    # Save model and encoders
    with open('model.pkl', 'wb') as f:
        pickle.dump((rf, encoders), f)

    return scores

def predict_salary(job_title, education, experience_years, industry, location):
    with open('model.pkl', 'rb') as f:
        model, encoders = pickle.load(f)

    job_enc = encoders['job'].transform([job_title])[0]
    edu_enc = encoders['edu'].transform([education])[0]
    ind_enc = encoders['ind'].transform([industry])[0]
    loc_enc = encoders['loc'].transform([location])[0]

    X = [[job_enc, edu_enc, experience_years, ind_enc, loc_enc]]
    salary = model.predict(X)[0]

    return round(salary, -3)

def get_options():
    return {
        'job_titles': ['Software Engineer', 'Data Analyst', 'Project Manager',
                       'IT Officer', 'System Administrator', 'Data Scientist',
                       'Web Developer', 'Network Engineer',
                       'Database Administrator', 'Business Analyst'],
        'education': ['High School', 'Bachelor', 'Master', 'PhD'],
        'industries': ['Technology', 'Finance', 'Healthcare', 'Education',
                       'Government', 'NGO', 'Telecommunications', 'Banking'],
        'locations': ['Kigali', 'Huye', 'Musanze', 'Rubavu', 'Nyagatare', 'Remote']
    }