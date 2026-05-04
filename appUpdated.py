# ============================================================================
# PLACEMENT READINESS & SKILL GAP ANALYTICS SYSTEM
# FDA EDITION — Foundations of Data Analytics
# ============================================================================
# Academic Project: Foundations of Data Analytics (FDA)
# Version: 3.0 — FULL FDA SYLLABUS INTEGRATION
# Tech Stack: Streamlit, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, SciPy
#
# FDA SYLLABUS COVERAGE (mapped to modules of the app)
# ----------------------------------------------------------------------------
#   Module 1 — Python Programming for Data Analytics
#       * Python basics: I/O, operators, control structure (used throughout)
#       * Lists / dictionaries / loops / functions (USERS_DATABASE, helpers)
#       * NumPy array operations (employability vectorization, normalization)
#       * Pandas: read CSV/Excel, indexing, filtering (Data Lab tab)
#
#   Module 2 — Data Wrangling
#       * Load structured & unstructured datasets (CSV upload, JSON parsing)
#       * Handle missing values & outliers (IQR, z-score, imputation)
#       * Data normalization & encoding (Min-Max, Z-score, Label/One-Hot)
#       * Feature creation & selection
#       * Dimensionality reduction using PCA (Wrangling Lab tab)
#
#   Module 3 — Exploratory Data Analysis (EDA) & Data Visualization
#       * Summary statistics (.describe(), custom NumPy stats)
#       * Histograms, boxplots, scatter, line, correlation heatmaps
#       * Time-series visualization with Pandas/Matplotlib/Seaborn
#
#   Module 4 — Machine Learning Basics
#       * Supervised: Logistic Regression placement predictor
#       * Unsupervised: KMeans student clustering
#
#   Module 5 — Statistical Foundations
#       * Mean, variance, standard deviation (NumPy)
#       * t-test, chi-square, ANOVA (SciPy)
#       * Correlation analysis (Pearson & Spearman)
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import io
import time

# Statistics (FDA Module 5)
from scipy import stats as sps

# Machine Learning (FDA Module 4) & Wrangling (Module 2)
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report, silhouette_score
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="FDA Placement Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

sns.set_theme(style="whitegrid", palette="viridis")

# ============================================================================
# CUSTOM CSS — modern glassy dashboard
# ============================================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
          radial-gradient(1200px 600px at 10% -10%, #1e3a8a33, transparent),
          radial-gradient(900px 500px at 110% 10%, #06b6d433, transparent),
          linear-gradient(180deg, #0b1220 0%, #0e1628 100%);
        color: #e6edf7;
    }
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        padding: 22px 10px 6px 10px;
        background: linear-gradient(90deg, #60a5fa 0%, #22d3ee 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    .sub-tagline {
        text-align: center;
        color: #93a4c3;
        margin-bottom: 18px;
        font-size: 0.95rem;
    }
    .fda-chip {
        display: inline-block;
        padding: 4px 10px;
        margin: 2px 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        color: #93c5fd;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .glass-card {
        background: rgba(17, 25, 40, 0.55);
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 10px 30px rgba(2, 6, 23, 0.45);
    }
    .metric-num {
        font-size: 1.8rem;
        font-weight: 800;
        color: #e2e8f0;
    }
    .metric-label {
        color: #93a4c3;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    .admin-badge {
        background: linear-gradient(90deg,#dc2626,#f59e0b);
        color: white; padding: 4px 12px; border-radius: 999px;
        font-weight: 700; font-size: 0.8rem;
    }
    .student-badge {
        background: linear-gradient(90deg,#10b981,#22d3ee);
        color: #062a26; padding: 4px 12px; border-radius: 999px;
        font-weight: 700; font-size: 0.8rem;
    }
    .section-title {
        font-size: 1.35rem; font-weight: 800; color: #e2e8f0;
        margin: 6px 0 10px 0;
    }
    .small-muted { color:#93a4c3; font-size:0.85rem; }
    div[data-testid="stMetric"] {
        background: rgba(15,23,42,0.6);
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 14px; padding: 12px 14px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(15,23,42,0.6);
        border-radius: 12px; padding: 10px 16px;
        color: #cbd5e1;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg,#1d4ed8,#0891b2) !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# USERS DATABASE  (FDA Module 1: dictionaries)
# ============================================================================

USERS_DATABASE = {
    "admin": {
        "password": "admin123", "role": "admin",
        "name": "System Administrator", "email": "admin@placement.edu",
    },
    "student": {
        "password": "1234", "role": "student",
        "name": "Student One", "email": "student@university.edu",
        "cgpa": 7.5, "profile_data": {},
    },
    "alice": {
        "password": "alice123", "role": "student",
        "name": "Alice Sharma", "email": "alice@university.edu",
        "cgpa": 8.8, "profile_data": {},
    },
    "bob": {
        "password": "bob123", "role": "student",
        "name": "Bob Wilson", "email": "bob@university.edu",
        "cgpa": 7.0, "profile_data": {},
    },
    "neha": {
        "password": "neha123", "role": "student",
        "name": "Neha Verma", "email": "neha@university.edu",
        "cgpa": 9.1, "profile_data": {},
    },
}

# ============================================================================
# COMPANY DATASET (used for placement matching)  — FDA Module 1: Pandas
# ============================================================================

def load_company_dataset() -> pd.DataFrame:
    """Build a structured Pandas DataFrame of recruiting companies."""
    companies_data = {
        "Company": [
            "Google", "Amazon", "Microsoft", "Apple", "Meta",
            "TCS", "Infosys", "Wipro", "Cognizant", "Accenture",
            "Adobe", "Oracle", "Salesforce", "IBM", "Capgemini",
            "HCL", "Tech Mahindra", "Flipkart", "Paytm", "Zomato",
            "Netflix", "Uber", "Airbnb", "Spotify", "LinkedIn",
        ],
        "Type": [
            "Product", "Product", "Product", "Product", "Product",
            "Service", "Service", "Service", "Service", "Service",
            "Product", "Product", "Product", "Service", "Service",
            "Service", "Service", "Product", "Product", "Product",
            "Product", "Product", "Product", "Product", "Product",
        ],
        "Min_CGPA": [
            8.5, 8.0, 8.2, 8.5, 8.3,
            6.5, 6.0, 6.2, 6.5, 6.8,
            8.0, 7.5, 7.8, 7.0, 6.5,
            6.0, 6.3, 7.5, 7.0, 6.8,
            8.0, 7.8, 8.2, 7.5, 8.0,
        ],
        "Max_Backlogs": [
            0, 0, 0, 0, 0,
            2, 3, 2, 2, 1,
            0, 1, 1, 2, 2,
            3, 3, 1, 1, 2,
            0, 0, 0, 1, 0,
        ],
        "Required_Skills": [
            ["DSA", "Python", "System Design", "Cloud"],
            ["DSA", "Java", "AWS", "SQL"],
            ["DSA", "C++", "Azure", "OOP"],
            ["DSA", "Swift", "iOS Development", "Python"],
            ["DSA", "Python", "React", "System Design"],
            ["Python", "SQL", "Testing"],
            ["Java", "DBMS", "Spring Boot"],
            ["Python", "SQL", "Cloud"],
            ["Java", "SQL", "Web Development"],
            ["Python", "Cloud", "DevOps"],
            ["DSA", "Java", "UI/UX", "Python"],
            ["SQL", "Java", "Database Management"],
            ["Java", "Cloud", "CRM"],
            ["Python", "AI/ML", "Cloud"],
            ["Java", "SAP", "Cloud"],
            ["Python", "Testing", "Automation"],
            ["Java", "Networking", "5G"],
            ["DSA", "Python", "Backend Development"],
            ["Python", "Payment Gateway", "Backend Development"],
            ["Python", "Backend Development", "Microservices"],
            ["DSA", "Python", "Microservices", "System Design"],
            ["DSA", "Go", "Distributed Systems", "Cloud"],
            ["DSA", "Python", "React", "Mobile Development"],
            ["DSA", "Python", "Audio Processing", "Cloud"],
            ["DSA", "Java", "Big Data", "System Design"],
        ],
        "Salary_LPA": [
            45, 42, 40, 48, 44,
            3.5, 4.0, 3.8, 4.2, 5.0,
            12, 10, 14, 8, 6,
            4.5, 5.5, 15, 12, 10,
            50, 38, 42, 35, 40,
        ],
        "Job_Role": [
            "Software Engineer", "SDE", "Software Developer", "iOS Developer", "Software Engineer",
            "IT Analyst", "System Engineer", "Project Engineer", "Programmer Analyst", "Application Developer",
            "Software Engineer", "Associate Consultant", "Developer", "Application Developer", "Analyst",
            "Software Engineer", "Engineer", "Backend Developer", "Software Developer", "Backend Developer",
            "Senior Software Engineer", "Software Engineer", "Full Stack Developer", "Backend Engineer", "Software Engineer",
        ],
        "Location": [
            "Bangalore", "Bangalore", "Hyderabad", "Bangalore", "Bangalore",
            "Multiple", "Bangalore", "Pune", "Chennai", "Bangalore",
            "Bangalore", "Bangalore", "Bangalore", "Multiple", "Multiple",
            "Noida", "Pune", "Bangalore", "Noida", "Gurgaon",
            "Mumbai", "Bangalore", "Bangalore", "Mumbai", "Bangalore",
        ],
        "Industry": [
            "Technology", "E-commerce", "Technology", "Technology", "Social Media",
            "IT Services", "IT Services", "IT Services", "IT Services", "Consulting",
            "Software", "Enterprise Software", "Cloud/CRM", "Technology", "Consulting",
            "IT Services", "Telecom", "E-commerce", "Fintech", "Food Tech",
            "Streaming", "Ride Sharing", "Travel Tech", "Music Streaming", "Professional Network",
        ],
        "Openings": [
            50, 80, 60, 30, 45,
            200, 250, 150, 180, 120,
            40, 50, 35, 100, 90,
            180, 140, 70, 60, 50,
            25, 45, 30, 28, 38,
        ],
    }
    return pd.DataFrame(companies_data)


# ============================================================================
# SYNTHETIC STUDENT DATASET — for EDA / ML / Stats (FDA Modules 3, 4, 5)
# ============================================================================

@st.cache_data(show_spinner=False)
def generate_student_dataset(n: int = 400, seed: int = 42) -> pd.DataFrame:
    """
    Build a realistic synthetic dataset of students.
    Uses NumPy random generators (FDA Module 1: NumPy array operations).
    """
    rng = np.random.default_rng(seed)

    cgpa = np.clip(rng.normal(7.4, 1.0, n), 4.0, 10.0)
    backlogs = rng.poisson(0.6, n).clip(0, 6)
    internships = rng.integers(0, 4, n)
    certifications = rng.integers(0, 8, n)
    projects = rng.integers(0, 7, n)
    coding_score = np.clip(rng.normal(60, 18, n) + (cgpa - 7) * 5, 0, 100)
    aptitude = np.clip(rng.normal(65, 15, n), 0, 100)
    communication = np.clip(rng.normal(62, 14, n), 0, 100)
    branches = rng.choice(
        ["CSE", "IT", "ECE", "EEE", "MECH"], n, p=[0.35, 0.20, 0.20, 0.15, 0.10]
    )
    gender = rng.choice(["Male", "Female"], n, p=[0.6, 0.4])

    # latent placement signal
    z = (
        (cgpa - 6.5) * 1.1
        - backlogs * 0.6
        + internships * 0.5
        + certifications * 0.15
        + projects * 0.2
        + (coding_score - 50) * 0.05
        + (aptitude - 55) * 0.04
        + (communication - 55) * 0.03
        + rng.normal(0, 0.6, n)
    )
    placed = (z > 1.2).astype(int)
    salary = np.where(placed == 1,
                      np.clip(rng.normal(8, 6, n) + (cgpa - 7) * 2, 3, 60),
                      0.0)

    df = pd.DataFrame({
        "Student_ID": [f"S{1000+i}" for i in range(n)],
        "Branch": branches,
        "Gender": gender,
        "CGPA": np.round(cgpa, 2),
        "Backlogs": backlogs,
        "Internships": internships,
        "Certifications": certifications,
        "Projects": projects,
        "Coding_Score": np.round(coding_score, 1),
        "Aptitude_Score": np.round(aptitude, 1),
        "Communication": np.round(communication, 1),
        "Placed": placed,
        "Salary_LPA": np.round(salary, 2),
    })

    # Inject some missing values & outliers (for Wrangling Lab demo)
    miss_idx = rng.choice(n, size=max(1, n // 25), replace=False)
    df.loc[miss_idx, "Communication"] = np.nan
    miss_idx2 = rng.choice(n, size=max(1, n // 30), replace=False)
    df.loc[miss_idx2, "Certifications"] = np.nan
    out_idx = rng.choice(n, size=3, replace=False)
    df.loc[out_idx, "Coding_Score"] = 999  # extreme outlier

    return df


# ============================================================================
# TIME-SERIES PLACEMENT TREND (FDA Module 3: time-series visualization)
# ============================================================================

@st.cache_data(show_spinner=False)
def generate_placement_timeseries(seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=datetime.today(), periods=24, freq="MS")
    base = np.linspace(40, 75, len(dates))
    seasonal = 8 * np.sin(np.linspace(0, 6 * np.pi, len(dates)))
    noise = rng.normal(0, 4, len(dates))
    rate = np.clip(base + seasonal + noise, 20, 95)
    return pd.DataFrame({"Month": dates, "PlacementRate": np.round(rate, 1)})


# ============================================================================
# SKILL CATEGORIES
# ============================================================================

PROGRAMMING_LANGUAGES = [
    "Python", "Java", "C++", "C", "JavaScript",
    "Go", "Rust", "Swift", "Kotlin", "R",
    "TypeScript", "Scala", "Ruby", "PHP", "Dart",
]

TECHNICAL_SKILLS = [
    "DSA", "System Design", "OOP", "DBMS", "SQL",
    "Cloud", "AWS", "Azure", "GCP", "DevOps",
    "Web Development", "Backend Development", "Frontend Development",
    "React", "Angular", "Node.js", "Django", "Flask",
    "Spring Boot", "Microservices", "REST API",
    "UI/UX", "Mobile Development", "iOS Development", "Android Development",
    "AI/ML", "Data Science", "Big Data", "Blockchain",
    "Testing", "Automation", "CI/CD", "Git", "Docker", "Kubernetes",
    "Networking", "5G", "Security", "Payment Gateway", "CRM", "SAP",
    "Database Management", "MongoDB", "Redis", "GraphQL",
    "Distributed Systems", "Audio Processing", "Video Processing",
]

SOFT_SKILLS = [
    "Communication", "Teamwork", "Leadership", "Problem Solving",
    "Time Management", "Adaptability", "Critical Thinking",
    "Presentation Skills", "Interpersonal Skills", "Work Ethic",
    "Creativity", "Collaboration", "Decision Making",
]

# ============================================================================
# SESSION STATE
# ============================================================================

def _init_state():
    defaults = {
        "logged_in": False,
        "username": "",
        "user_role": "",
        "analysis_done": False,
        "student_analyses": [],
        "uploaded_df": None,
        "wrangled_df": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def calculate_employability_score(cgpa, backlogs, prog_langs, tech_skills,
                                  soft_skills, certifications, internship,
                                  company_alignment):
    """
    Rule-based employability score (uses NumPy for vectorized weighting).
    FDA Module 1 — functions, NumPy.
    """
    weights = np.array([0.30, 0.25, 0.15, 0.10, 0.10, 0.10])  # cgpa, skills, intern, cert, soft, align
    cgpa_component       = (cgpa / 10.0) * 100
    total_skills         = len(prog_langs) + len(tech_skills)
    skills_component     = min(total_skills / 12.0 * 100, 100)
    internship_component = 100.0 if internship else 0.0
    cert_component       = min(certifications / 5.0 * 100, 100)
    soft_component       = min(len(soft_skills) / 6.0 * 100, 100)
    align_component      = float(np.clip(company_alignment, 0, 100))

    components = np.array([
        cgpa_component, skills_component, internship_component,
        cert_component, soft_component, align_component
    ])
    score = float(np.dot(weights, components))
    backlog_penalty = min(backlogs * 4, 20)
    score = max(score - backlog_penalty, 0.0)
    return round(score, 2), {
        "CGPA": cgpa_component,
        "Skills": skills_component,
        "Internship": internship_component,
        "Certifications": cert_component,
        "Soft Skills": soft_component,
        "Company Alignment": align_component,
    }


def get_eligible_companies(cgpa: float, backlogs: int, student_skills: list,
                            companies_df: pd.DataFrame) -> pd.DataFrame:
    """Filter companies via Pandas boolean indexing (FDA Module 1)."""
    df = companies_df.copy()
    student_skills_set = set([s.lower() for s in student_skills])

    def _match_pct(req):
        req_set = set([s.lower() for s in req])
        if not req_set: return 0.0
        return round(len(student_skills_set & req_set) / len(req_set) * 100, 1)

    df["Skill_Match_%"] = df["Required_Skills"].apply(_match_pct)
    df["Eligible"] = (
        (df["Min_CGPA"] <= cgpa) &
        (df["Max_Backlogs"] >= backlogs) &
        (df["Skill_Match_%"] >= 40)
    )
    eligible = df[df["Eligible"]].sort_values(
        ["Skill_Match_%", "Salary_LPA"], ascending=[False, False]
    )
    return eligible


def detect_skill_gap(student_skills: list, companies_df: pd.DataFrame, top_k: int = 10):
    """Find skills the student lacks against the most in-demand requirements."""
    all_required = []
    for skills in companies_df["Required_Skills"]:
        all_required.extend(skills)
    demand = pd.Series(all_required).value_counts()
    student_set = set([s.lower() for s in student_skills])
    gaps = [s for s in demand.index if s.lower() not in student_set]
    return demand.head(top_k), gaps[:top_k]


# ============================================================================
# SIDEBAR — LOGIN
# ============================================================================

def render_login():
    st.markdown('<div class="main-header">🎓 FDA Placement Analytics</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-tagline">'
        'A Foundations of Data Analytics project — Python • NumPy • Pandas • '
        'EDA • PCA • ML • Statistical Tests'
        '</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div style="text-align:center;">'
        '<span class="fda-chip">Module 1 · Python+NumPy+Pandas</span>'
        '<span class="fda-chip">Module 2 · Wrangling+PCA</span>'
        '<span class="fda-chip">Module 3 · EDA & Visualization</span>'
        '<span class="fda-chip">Module 4 · ML Basics</span>'
        '<span class="fda-chip">Module 5 · Stats (t/χ²/ANOVA/ρ)</span>'
        '</div><br>', unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Sign In")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pwd")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login", use_container_width=True, type="primary"):
                user = USERS_DATABASE.get(username)
                if user and user["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = user["role"]
                    st.success(f"Welcome, {user['name']}!")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        with c2:
            if st.button("Demo Student", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "alice"
                st.session_state.user_role = "student"
                st.rerun()

        with st.expander("Demo Accounts"):
            st.code(
                "admin / admin123     (Admin)\n"
                "student / 1234       (Student)\n"
                "alice / alice123     (Student)\n"
                "bob / bob123         (Student)\n"
                "neha / neha123       (Student)"
            )
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# SHARED HEADER
# ============================================================================

def render_header():
    user = USERS_DATABASE.get(st.session_state.username, {})
    role = st.session_state.user_role
    badge = ('<span class="admin-badge">ADMIN</span>' if role == "admin"
             else '<span class="student-badge">STUDENT</span>')
    cols = st.columns([6, 2, 1.5])
    with cols[0]:
        st.markdown('<div class="main-header">🎓 FDA Placement Analytics</div>',
                    unsafe_allow_html=True)
    with cols[1]:
        st.markdown(
            f'<div style="text-align:right;padding-top:24px;">'
            f'<span class="small-muted">Signed in as</span> '
            f'<b>{user.get("name","-")}</b> &nbsp;{badge}</div>',
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            for k in ["logged_in", "username", "user_role", "analysis_done"]:
                st.session_state[k] = False if isinstance(st.session_state.get(k), bool) else ""
            st.rerun()


# ============================================================================
# STUDENT — Profile & employability tab
# ============================================================================

def tab_student_profile(companies_df: pd.DataFrame):
    user = USERS_DATABASE.get(st.session_state.username, {})
    st.markdown('<div class="section-title">👤 Profile & Employability</div>',
                unsafe_allow_html=True)

    with st.form("profile_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            cgpa = st.number_input("CGPA", 0.0, 10.0, float(user.get("cgpa", 7.5)), 0.1)
            backlogs = st.number_input("Active backlogs", 0, 10, 0)
            internship = st.checkbox("Completed at least one internship", True)
        with c2:
            certifications = st.number_input("Certifications", 0, 30, 3)
            target_industry = st.selectbox(
                "Target industry",
                sorted(companies_df["Industry"].unique().tolist())
            )
            target_type = st.selectbox("Preferred company type",
                                       ["Product", "Service", "Any"])
        with c3:
            prog_langs = st.multiselect("Programming languages",
                                        PROGRAMMING_LANGUAGES,
                                        default=["Python", "Java"])
            tech_skills = st.multiselect("Technical skills",
                                         TECHNICAL_SKILLS,
                                         default=["DSA", "SQL", "Cloud"])
            soft_skills = st.multiselect("Soft skills", SOFT_SKILLS,
                                         default=["Communication", "Teamwork"])

        submitted = st.form_submit_button("🔎 Analyze My Placement Readiness",
                                          use_container_width=True, type="primary")

    if not submitted:
        return

    # Company alignment heuristic
    student_skills = prog_langs + tech_skills
    eligible = get_eligible_companies(cgpa, backlogs, student_skills, companies_df)
    align = float(eligible["Skill_Match_%"].mean()) if not eligible.empty else 0.0

    score, breakdown = calculate_employability_score(
        cgpa, backlogs, prog_langs, tech_skills, soft_skills,
        certifications, internship, align
    )

    st.session_state.analysis_done = True
    st.session_state.student_analyses.append({
        "username": st.session_state.username,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "score": score,
        "cgpa": cgpa, "backlogs": backlogs,
        "skills": student_skills, "eligible": int(len(eligible)),
    })

    # Headline metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Employability Score", f"{score}/100")
    with m2: st.metric("Eligible Companies", len(eligible))
    with m3: st.metric("Avg Skill Match", f"{align:.1f}%")
    with m4:
        tier = "🏆 Excellent" if score >= 80 else "✅ Good" if score >= 65 else "⚠️ Improve" if score >= 50 else "🚧 At Risk"
        st.metric("Tier", tier)

    # Score breakdown — Matplotlib bar chart
    st.markdown("#### Score Breakdown")
    fig, ax = plt.subplots(figsize=(9, 3.6))
    keys = list(breakdown.keys()); vals = list(breakdown.values())
    colors = sns.color_palette("viridis", len(keys))
    ax.barh(keys, vals, color=colors)
    ax.set_xlim(0, 100); ax.set_xlabel("Score (0-100)")
    ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.text(v + 1, i, f"{v:.0f}", va="center", fontsize=9)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

    # Eligible companies
    st.markdown("#### 🎯 Eligible Companies (Pandas filtering)")
    if eligible.empty:
        st.warning("No eligible companies yet. Improve CGPA or add high-demand skills.")
    else:
        if target_type != "Any":
            view = eligible[eligible["Type"] == target_type]
        else:
            view = eligible
        st.dataframe(
            view[["Company", "Type", "Job_Role", "Industry", "Min_CGPA",
                  "Max_Backlogs", "Salary_LPA", "Skill_Match_%", "Openings"]]
            .reset_index(drop=True),
            use_container_width=True, height=320,
        )

    # Skill gap
    st.markdown("#### 🧩 Skill Gap Analysis")
    demand, gaps = detect_skill_gap(student_skills, companies_df, 12)
    g1, g2 = st.columns([1.2, 1])
    with g1:
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(x=demand.values, y=demand.index, ax=ax, palette="rocket")
        ax.set_xlabel("Companies requiring skill")
        ax.set_title("Top in-demand skills")
        fig.tight_layout()
        st.pyplot(fig, clear_figure=True)
    with g2:
        st.markdown("**Skills you should learn next:**")
        if not gaps:
            st.success("No major gaps detected. Polish existing skills!")
        else:
            for g in gaps:
                st.markdown(f"- 🔧 **{g}**")


# ============================================================================
# DATA LAB — Pandas (FDA Module 1)
# ============================================================================

def tab_data_lab():
    st.markdown('<div class="section-title">🧪 Data Lab — Pandas / NumPy</div>',
                unsafe_allow_html=True)
    st.caption("FDA Module 1 — read CSV/Excel, indexing, filtering · NumPy array ops")

    src = st.radio("Choose data source",
                   ["Synthetic student dataset", "Upload CSV", "Upload Excel"],
                   horizontal=True)

    df = None
    if src == "Synthetic student dataset":
        df = generate_student_dataset()
    elif src == "Upload CSV":
        f = st.file_uploader("Upload CSV", type=["csv"], key="csv_up")
        if f is not None:
            df = pd.read_csv(f)
    else:
        f = st.file_uploader("Upload Excel", type=["xlsx", "xls"], key="xls_up")
        if f is not None:
            df = pd.read_excel(f)

    if df is None:
        st.info("Load a dataset to continue.")
        return

    st.session_state.uploaded_df = df

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Rows", df.shape[0])
    with c2: st.metric("Columns", df.shape[1])
    with c3: st.metric("Numeric cols", df.select_dtypes(include=np.number).shape[1])
    with c4: st.metric("Missing cells", int(df.isna().sum().sum()))

    st.markdown("##### Preview (df.head)")
    st.dataframe(df.head(10), use_container_width=True)

    with st.expander("📐 NumPy Array Operations on a numeric column"):
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if num_cols:
            col = st.selectbox("Pick numeric column", num_cols, key="np_col")
            arr = df[col].dropna().to_numpy()
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("mean", f"{arr.mean():.3f}")
            with c2: st.metric("std",  f"{arr.std():.3f}")
            with c3: st.metric("min",  f"{arr.min():.3f}")
            with c4: st.metric("max",  f"{arr.max():.3f}")
            st.write("Reshape demo: first 12 elements →")
            sub = arr[:12] if len(arr) >= 12 else arr
            st.code(np.array2string(sub.reshape(-1, min(4, len(sub))),
                                    precision=2, separator=", "))

    with st.expander("🔍 Pandas Indexing & Filtering"):
        st.write("Use a query string (Pandas `.query`) — e.g. `CGPA > 8 and Backlogs == 0`")
        q = st.text_input("Query", value="CGPA > 8 and Backlogs == 0"
                          if "CGPA" in df.columns else "")
        if q:
            try:
                st.dataframe(df.query(q), use_container_width=True, height=280)
            except Exception as e:
                st.error(f"Query error: {e}")


# ============================================================================
# WRANGLING LAB — FDA Module 2
# ============================================================================

def tab_wrangling_lab():
    st.markdown('<div class="section-title">🧹 Data Wrangling Lab</div>',
                unsafe_allow_html=True)
    st.caption("FDA Module 2 — missing values · outliers · normalization · encoding · PCA")

    df = st.session_state.uploaded_df
    if df is None:
        st.info("Load a dataset in the Data Lab tab first.")
        return

    work = df.copy()
    st.markdown("#### 1️⃣ Missing Value Handling")
    miss = work.isna().sum()
    miss = miss[miss > 0]
    cmiss1, cmiss2 = st.columns([1, 1.3])
    with cmiss1:
        if miss.empty:
            st.success("No missing values detected.")
        else:
            st.dataframe(miss.rename("missing").to_frame(), use_container_width=True)
        strategy = st.radio(
            "Imputation strategy",
            ["Drop rows", "Mean (numeric)", "Median (numeric)", "Mode (all)"],
            horizontal=False,
        )
    with cmiss2:
        if not miss.empty:
            fig, ax = plt.subplots(figsize=(6, 3))
            sns.heatmap(work.isna().iloc[:, :30], cbar=False, ax=ax, cmap="mako")
            ax.set_title("Missingness pattern (first 30 cols)")
            fig.tight_layout()
            st.pyplot(fig, clear_figure=True)

    if strategy == "Drop rows":
        work = work.dropna()
    elif strategy == "Mean (numeric)":
        for c in work.select_dtypes(include=np.number).columns:
            work[c] = work[c].fillna(work[c].mean())
    elif strategy == "Median (numeric)":
        for c in work.select_dtypes(include=np.number).columns:
            work[c] = work[c].fillna(work[c].median())
    else:
        for c in work.columns:
            work[c] = work[c].fillna(work[c].mode().iloc[0] if not work[c].mode().empty else 0)

    st.markdown("#### 2️⃣ Outlier Detection")
    num_cols = work.select_dtypes(include=np.number).columns.tolist()
    if num_cols:
        col = st.selectbox("Numeric column", num_cols, key="out_col")
        method = st.radio("Method", ["IQR (1.5×)", "Z-score (>|3|)"], horizontal=True)
        series = work[col].dropna()
        if method.startswith("IQR"):
            q1, q3 = np.percentile(series, [25, 75])
            iqr = q3 - q1
            lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            mask = (work[col] < lo) | (work[col] > hi)
        else:
            z = np.abs(sps.zscore(series, nan_policy="omit"))
            mask_idx = series.index[z > 3]
            mask = work.index.isin(mask_idx)
        n_out = int(np.sum(mask))
        st.write(f"Detected **{n_out}** outliers in `{col}`.")
        co1, co2 = st.columns(2)
        with co1:
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.boxplot(x=work[col], ax=ax, color="#22d3ee")
            ax.set_title(f"Boxplot — {col}")
            fig.tight_layout(); st.pyplot(fig, clear_figure=True)
        with co2:
            if st.button("Remove detected outliers"):
                work = work[~mask]
                st.success(f"Removed {n_out} rows.")

    st.markdown("#### 3️⃣ Normalization & Encoding")
    n1, n2 = st.columns(2)
    with n1:
        norm = st.selectbox("Numeric scaling",
                            ["None", "Min-Max (0-1)", "Z-score (Standard)"])
        if norm != "None" and num_cols:
            scaler = MinMaxScaler() if norm.startswith("Min") else StandardScaler()
            work[num_cols] = scaler.fit_transform(work[num_cols])
            st.success(f"Applied {norm}.")
    with n2:
        cat_cols = work.select_dtypes(exclude=np.number).columns.tolist()
        encoding = st.selectbox("Categorical encoding",
                                ["None", "Label Encoding", "One-Hot Encoding"])
        if encoding == "Label Encoding" and cat_cols:
            for c in cat_cols:
                work[c] = LabelEncoder().fit_transform(work[c].astype(str))
            st.success("Label encoded.")
        elif encoding == "One-Hot Encoding" and cat_cols:
            work = pd.get_dummies(work, columns=cat_cols, drop_first=True)
            st.success("One-hot encoded.")

    st.markdown("#### 4️⃣ Feature Creation")
    if {"Internships", "Certifications", "Projects"}.issubset(work.columns):
        if st.checkbox("Create `Experience_Index = Internships + 0.5·Certifications + 0.7·Projects`"):
            work["Experience_Index"] = (
                work["Internships"] + 0.5 * work["Certifications"] + 0.7 * work["Projects"]
            )
            st.success("Feature added.")

    st.markdown("#### 5️⃣ Dimensionality Reduction — PCA")
    nums = work.select_dtypes(include=np.number).dropna(axis=1, how="any")
    if nums.shape[1] >= 3:
        ncomp = st.slider("PCA components", 2, min(6, nums.shape[1]), 2)
        X = StandardScaler().fit_transform(nums)
        pca = PCA(n_components=ncomp)
        comps = pca.fit_transform(X)
        evr = pca.explained_variance_ratio_

        cP1, cP2 = st.columns([1, 1])
        with cP1:
            fig, ax = plt.subplots(figsize=(5, 3.5))
            ax.bar(range(1, ncomp + 1), evr, color="#60a5fa")
            ax.plot(range(1, ncomp + 1), np.cumsum(evr), marker="o", color="#f59e0b")
            ax.set_xlabel("Component"); ax.set_ylabel("Explained variance")
            ax.set_title("PCA Scree + Cumulative")
            fig.tight_layout(); st.pyplot(fig, clear_figure=True)
        with cP2:
            fig, ax = plt.subplots(figsize=(5, 3.5))
            color_col = None
            if "Placed" in df.columns and len(df) == len(comps):
                color_col = df["Placed"].values
            sc = ax.scatter(comps[:, 0], comps[:, 1],
                            c=color_col if color_col is not None else "#22d3ee",
                            cmap="coolwarm", alpha=0.7, s=24)
            ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
            ax.set_title("PCA Projection (PC1 vs PC2)")
            if color_col is not None:
                plt.colorbar(sc, ax=ax, label="Placed")
            fig.tight_layout(); st.pyplot(fig, clear_figure=True)

        st.caption(f"Total variance captured by {ncomp} components: "
                   f"**{np.sum(evr)*100:.1f}%**")

    st.session_state.wrangled_df = work
    with st.expander("📤 Download wrangled dataset"):
        buf = io.StringIO(); work.to_csv(buf, index=False)
        st.download_button("Download CSV", buf.getvalue(),
                           file_name="wrangled.csv", mime="text/csv")


# ============================================================================
# EDA — FDA Module 3
# ============================================================================

def tab_eda():
    st.markdown('<div class="section-title">📊 Exploratory Data Analysis</div>',
                unsafe_allow_html=True)
    st.caption("FDA Module 3 — summary stats · histograms · boxplots · scatter · "
               "line charts · correlation heatmaps · time-series")

    df = st.session_state.uploaded_df
    if df is None:
        df = generate_student_dataset()

    st.markdown("#### 📋 Summary Statistics (`df.describe`)")
    st.dataframe(df.describe(include="all").T, use_container_width=True)

    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    st.markdown("#### 📈 Univariate Plots")
    c1, c2 = st.columns(2)
    with c1:
        col = st.selectbox("Histogram column", num_cols, key="hist_col")
        bins = st.slider("Bins", 5, 60, 25)
        fig, ax = plt.subplots(figsize=(5.5, 3.6))
        sns.histplot(df[col].dropna(), bins=bins, kde=True, ax=ax, color="#60a5fa")
        ax.set_title(f"Histogram — {col}")
        fig.tight_layout(); st.pyplot(fig, clear_figure=True)
    with c2:
        col2 = st.selectbox("Boxplot column", num_cols, key="box_col")
        group = st.selectbox("Group by (optional)", ["(none)"] + cat_cols, key="box_grp")
        fig, ax = plt.subplots(figsize=(5.5, 3.6))
        if group == "(none)":
            sns.boxplot(y=df[col2], ax=ax, color="#a78bfa")
        else:
            sns.boxplot(x=df[group], y=df[col2], ax=ax, palette="Set2")
            plt.xticks(rotation=20)
        ax.set_title(f"Boxplot — {col2}")
        fig.tight_layout(); st.pyplot(fig, clear_figure=True)

    st.markdown("#### 🔁 Bivariate — Scatter")
    if len(num_cols) >= 2:
        s1, s2, s3 = st.columns(3)
        with s1: x = st.selectbox("X", num_cols, index=0, key="sx")
        with s2: y = st.selectbox("Y", num_cols, index=1, key="sy")
        with s3: hue = st.selectbox("Hue", ["(none)"] + cat_cols + ["Placed"]
                                    if "Placed" in df.columns else ["(none)"] + cat_cols,
                                    key="shue")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.scatterplot(data=df, x=x, y=y,
                        hue=None if hue == "(none)" else hue,
                        palette="viridis", ax=ax, alpha=0.75)
        ax.set_title(f"{y} vs {x}")
        fig.tight_layout(); st.pyplot(fig, clear_figure=True)

    st.markdown("#### 🔥 Correlation Heatmap")
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(min(10, 0.7 * len(num_cols) + 3),
                                        min(7, 0.5 * len(num_cols) + 2)))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                    ax=ax, cbar_kws={"shrink": 0.8})
        ax.set_title("Pearson correlation")
        fig.tight_layout(); st.pyplot(fig, clear_figure=True)

    st.markdown("#### ⏱️ Time-Series — Placement Rate (last 24 months)")
    ts = generate_placement_timeseries()
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(ts["Month"], ts["PlacementRate"], color="#22d3ee", linewidth=2)
    ax.fill_between(ts["Month"], ts["PlacementRate"], alpha=0.18, color="#22d3ee")
    rolling = ts["PlacementRate"].rolling(3).mean()
    ax.plot(ts["Month"], rolling, color="#f59e0b", linewidth=2, linestyle="--",
            label="3-month moving average")
    ax.set_ylabel("Placement Rate (%)"); ax.legend()
    ax.set_title("Placement rate over time")
    fig.autofmt_xdate()
    fig.tight_layout(); st.pyplot(fig, clear_figure=True)


# ============================================================================
# ML LAB — FDA Module 4
# ============================================================================

def tab_ml_lab():
    st.markdown('<div class="section-title">🤖 Machine Learning Lab</div>',
                unsafe_allow_html=True)
    st.caption("FDA Module 4 — supervised (Logistic Regression) & unsupervised (KMeans)")

    df = st.session_state.uploaded_df
    if df is None or "Placed" not in df.columns:
        df = generate_student_dataset()
        st.info("Using synthetic dataset (your uploaded data has no `Placed` target).")

    work = df.copy()
    work = work.dropna()
    feature_cols = ["CGPA", "Backlogs", "Internships", "Certifications",
                    "Projects", "Coding_Score", "Aptitude_Score", "Communication"]
    feature_cols = [c for c in feature_cols if c in work.columns]

    tab_sup, tab_unsup = st.tabs(["📌 Supervised — Placement Predictor",
                                  "🌀 Unsupervised — Student Clusters"])

    # ---------- Supervised ----------
    with tab_sup:
        st.markdown("**Goal:** Predict whether a student will be placed.")
        test_size = st.slider("Test size", 0.1, 0.5, 0.25, 0.05)
        X = work[feature_cols].values
        y = work["Placed"].values
        X = StandardScaler().fit_transform(X)

        Xtr, Xte, ytr, yte = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        model = LogisticRegression(max_iter=500)
        model.fit(Xtr, ytr)
        ypred = model.predict(Xte)
        acc = accuracy_score(yte, ypred)

        c1, c2 = st.columns([1, 1.3])
        with c1:
            st.metric("Test accuracy", f"{acc*100:.1f}%")
            st.write("**Coefficients (importance)**")
            imp = pd.DataFrame({
                "feature": feature_cols,
                "coef": model.coef_[0],
            }).sort_values("coef", key=abs, ascending=False)
            fig, ax = plt.subplots(figsize=(5, 3.6))
            sns.barplot(data=imp, y="feature", x="coef",
                        ax=ax, palette="vlag")
            ax.axvline(0, color="#888", linewidth=0.8)
            ax.set_title("Logistic Regression coefficients")
            fig.tight_layout(); st.pyplot(fig, clear_figure=True)
        with c2:
            cm = confusion_matrix(yte, ypred)
            fig, ax = plt.subplots(figsize=(4, 3.4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                        xticklabels=["Not Placed", "Placed"],
                        yticklabels=["Not Placed", "Placed"])
            ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
            ax.set_title("Confusion Matrix")
            fig.tight_layout(); st.pyplot(fig, clear_figure=True)
            st.text(classification_report(yte, ypred,
                                          target_names=["Not Placed", "Placed"]))

        st.markdown("##### 🎯 Try a prediction")
        cols = st.columns(len(feature_cols))
        sample_vals = []
        for i, fc in enumerate(feature_cols):
            with cols[i]:
                v = st.number_input(fc, value=float(work[fc].mean()), key=f"pr_{fc}")
                sample_vals.append(v)
        if st.button("Predict placement", type="primary"):
            sx = StandardScaler().fit(work[feature_cols].values).transform([sample_vals])
            prob = model.predict_proba(sx)[0, 1]
            verdict = "✅ Likely Placed" if prob >= 0.5 else "⚠️ Unlikely"
            st.success(f"{verdict} — probability = {prob*100:.1f}%")

    # ---------- Unsupervised ----------
    with tab_unsup:
        st.markdown("**Goal:** Discover natural student segments via KMeans.")
        k = st.slider("Number of clusters (k)", 2, 6, 3)
        X = StandardScaler().fit_transform(work[feature_cols].values)
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = km.fit_predict(X)
        sil = silhouette_score(X, labels) if k > 1 else 0.0

        st.metric("Silhouette score", f"{sil:.3f}")

        # 2D PCA projection
        proj = PCA(n_components=2).fit_transform(X)
        fig, ax = plt.subplots(figsize=(7.5, 4.2))
        sc = ax.scatter(proj[:, 0], proj[:, 1], c=labels, cmap="tab10",
                        alpha=0.8, s=28)
        ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
        ax.set_title(f"KMeans clusters (k={k}) on PCA projection")
        legend1 = ax.legend(*sc.legend_elements(), title="Cluster",
                            loc="best")
        ax.add_artist(legend1)
        fig.tight_layout(); st.pyplot(fig, clear_figure=True)

        # Cluster profiles
        prof = work[feature_cols].copy()
        prof["cluster"] = labels
        st.markdown("##### Cluster centroids (mean of features)")
        st.dataframe(prof.groupby("cluster").mean().round(2),
                     use_container_width=True)


# ============================================================================
# STATS LAB — FDA Module 5
# ============================================================================

def tab_stats_lab():
    st.markdown('<div class="section-title">📐 Statistical Foundations</div>',
                unsafe_allow_html=True)
    st.caption("FDA Module 5 — mean/var/std · t-test · χ² · ANOVA · Pearson & Spearman")

    df = st.session_state.uploaded_df
    if df is None:
        df = generate_student_dataset()

    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    # Descriptive
    st.markdown("#### 1️⃣ Descriptive Statistics (NumPy)")
    if num_cols:
        c = st.selectbox("Column", num_cols, key="desc_col")
        a = df[c].dropna().to_numpy()
        cols = st.columns(5)
        for col_box, name, val in zip(
            cols,
            ["Mean", "Variance", "Std Dev", "Skewness", "Kurtosis"],
            [np.mean(a), np.var(a), np.std(a),
             sps.skew(a), sps.kurtosis(a)],
        ):
            col_box.metric(name, f"{val:.3f}")

    st.markdown("---")

    # T-test
    st.markdown("#### 2️⃣ Independent t-test")
    st.caption("Compare a numeric column across two groups of a categorical column.")
    if num_cols and cat_cols:
        nc = st.selectbox("Numeric variable", num_cols, key="t_num")
        cc = st.selectbox("Group variable (binary preferred)", cat_cols, key="t_cat")
        groups = df[cc].dropna().unique().tolist()
        if len(groups) >= 2:
            g1, g2 = st.columns(2)
            with g1: a_lbl = st.selectbox("Group A", groups, key="t_a")
            with g2: b_lbl = st.selectbox("Group B",
                                          [g for g in groups if g != a_lbl],
                                          key="t_b")
            a = df.loc[df[cc] == a_lbl, nc].dropna()
            b = df.loc[df[cc] == b_lbl, nc].dropna()
            if len(a) > 1 and len(b) > 1:
                t_stat, p = sps.ttest_ind(a, b, equal_var=False)
                m1, m2, m3 = st.columns(3)
                m1.metric("t-statistic", f"{t_stat:.3f}")
                m2.metric("p-value", f"{p:.4f}")
                m3.metric("Significant? (α=0.05)",
                          "✅ Yes" if p < 0.05 else "❌ No")

    st.markdown("---")

    # Chi-square
    st.markdown("#### 3️⃣ Chi-square Test of Independence")
    if len(cat_cols) >= 2:
        c1, c2 = st.columns(2)
        with c1: a_col = st.selectbox("Categorical A", cat_cols, key="chi_a")
        with c2: b_col = st.selectbox("Categorical B",
                                      [c for c in cat_cols if c != a_col],
                                      key="chi_b")
        ct = pd.crosstab(df[a_col], df[b_col])
        st.dataframe(ct, use_container_width=True)
        if ct.size:
            chi2, p, dof, _ = sps.chi2_contingency(ct)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("χ²", f"{chi2:.3f}")
            m2.metric("dof", f"{dof}")
            m3.metric("p-value", f"{p:.4f}")
            m4.metric("Independent?", "❌ No (related)" if p < 0.05 else "✅ Yes")

    st.markdown("---")

    # ANOVA
    st.markdown("#### 4️⃣ One-way ANOVA")
    if num_cols and cat_cols:
        nc = st.selectbox("Numeric variable", num_cols, key="an_num")
        cc = st.selectbox("Group variable (≥3 groups ideal)", cat_cols, key="an_cat")
        groups = [df.loc[df[cc] == g, nc].dropna().values
                  for g in df[cc].dropna().unique()]
        groups = [g for g in groups if len(g) > 1]
        if len(groups) >= 2:
            F, p = sps.f_oneway(*groups)
            m1, m2, m3 = st.columns(3)
            m1.metric("F-statistic", f"{F:.3f}")
            m2.metric("p-value", f"{p:.4f}")
            m3.metric("Group means differ?",
                      "✅ Yes" if p < 0.05 else "❌ No")

            fig, ax = plt.subplots(figsize=(7, 3.6))
            sns.boxplot(x=df[cc], y=df[nc], ax=ax, palette="Set3")
            ax.set_title(f"{nc} across {cc}")
            plt.xticks(rotation=20)
            fig.tight_layout(); st.pyplot(fig, clear_figure=True)

    st.markdown("---")

    # Correlations
    st.markdown("#### 5️⃣ Correlation — Pearson & Spearman")
    if len(num_cols) >= 2:
        c1, c2 = st.columns(2)
        with c1: x = st.selectbox("Variable X", num_cols, key="corx")
        with c2: y = st.selectbox("Variable Y",
                                  [c for c in num_cols if c != x], key="cory")
        sub = df[[x, y]].dropna()
        if len(sub) > 2:
            pe = sps.pearsonr(sub[x], sub[y])
            sp = sps.spearmanr(sub[x], sub[y])
            cc1, cc2, cc3, cc4 = st.columns(4)
            cc1.metric("Pearson r", f"{pe.statistic:.3f}")
            cc2.metric("Pearson p", f"{pe.pvalue:.4f}")
            cc3.metric("Spearman ρ", f"{sp.statistic:.3f}")
            cc4.metric("Spearman p", f"{sp.pvalue:.4f}")
            fig, ax = plt.subplots(figsize=(6.5, 3.8))
            sns.regplot(data=sub, x=x, y=y, ax=ax,
                        scatter_kws={"alpha": 0.6, "color": "#60a5fa"},
                        line_kws={"color": "#f59e0b"})
            ax.set_title(f"Regression line: {y} vs {x}")
            fig.tight_layout(); st.pyplot(fig, clear_figure=True)


# ============================================================================
# COMPANIES TAB
# ============================================================================

def tab_companies(companies_df: pd.DataFrame):
    st.markdown('<div class="section-title">🏢 Companies Explorer</div>',
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        types = st.multiselect("Type", companies_df["Type"].unique(),
                               default=list(companies_df["Type"].unique()))
    with c2:
        industries = st.multiselect("Industry",
                                    companies_df["Industry"].unique(),
                                    default=list(companies_df["Industry"].unique()))
    with c3:
        max_cgpa = st.slider("Max required CGPA", 6.0, 10.0, 10.0, 0.1)

    view = companies_df[
        companies_df["Type"].isin(types)
        & companies_df["Industry"].isin(industries)
        & (companies_df["Min_CGPA"] <= max_cgpa)
    ].copy()
    view["Required_Skills"] = view["Required_Skills"].apply(", ".join)
    st.dataframe(view.reset_index(drop=True), use_container_width=True, height=420)

    # Quick chart: salary by type
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    sns.boxplot(data=companies_df, x="Type", y="Salary_LPA",
                ax=ax, palette="Set2")
    ax.set_title("Salary distribution by company type")
    fig.tight_layout(); st.pyplot(fig, clear_figure=True)


# ============================================================================
# ADMIN — analytics overview
# ============================================================================

def tab_admin_overview(companies_df: pd.DataFrame):
    st.markdown('<div class="section-title">🛡️ Admin Overview</div>',
                unsafe_allow_html=True)

    students = generate_student_dataset()
    placed_rate = students["Placed"].mean() * 100
    avg_cgpa = students["CGPA"].mean()
    avg_salary_placed = students.loc[students["Placed"] == 1, "Salary_LPA"].mean()

    m = st.columns(5)
    m[0].metric("Students", f"{len(students)}")
    m[1].metric("Placement Rate", f"{placed_rate:.1f}%")
    m[2].metric("Avg CGPA", f"{avg_cgpa:.2f}")
    m[3].metric("Avg Salary (LPA)", f"{avg_salary_placed:.2f}")
    m[4].metric("Companies", f"{len(companies_df)}")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        rate = students.groupby("Branch")["Placed"].mean() * 100
        sns.barplot(x=rate.index, y=rate.values, ax=ax, palette="viridis")
        ax.set_ylabel("Placement Rate (%)")
        ax.set_title("Placement rate by branch")
        fig.tight_layout(); st.pyplot(fig, clear_figure=True)
    with c2:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        sns.histplot(students.loc[students["Placed"] == 1, "Salary_LPA"],
                     bins=20, ax=ax, color="#22d3ee", kde=True)
        ax.set_title("Salary distribution (placed)")
        fig.tight_layout(); st.pyplot(fig, clear_figure=True)

    st.markdown("##### Recent student analyses (this session)")
    if st.session_state.student_analyses:
        st.dataframe(pd.DataFrame(st.session_state.student_analyses),
                     use_container_width=True)
    else:
        st.info("No analyses logged in this session yet.")


# ============================================================================
# MAIN
# ============================================================================

def main():
    if not st.session_state.logged_in:
        render_login()
        return

    render_header()
    companies_df = load_company_dataset()

    if st.session_state.user_role == "student":
        tabs = st.tabs([
            "👤 Profile",
            "🧪 Data Lab",
            "🧹 Wrangling",
            "📊 EDA",
            "🤖 ML Lab",
            "📐 Stats Lab",
            "🏢 Companies",
        ])
        with tabs[0]: tab_student_profile(companies_df)
        with tabs[1]: tab_data_lab()
        with tabs[2]: tab_wrangling_lab()
        with tabs[3]: tab_eda()
        with tabs[4]: tab_ml_lab()
        with tabs[5]: tab_stats_lab()
        with tabs[6]: tab_companies(companies_df)
    else:
        tabs = st.tabs([
            "🛡️ Overview",
            "🧪 Data Lab",
            "🧹 Wrangling",
            "📊 EDA",
            "🤖 ML Lab",
            "📐 Stats Lab",
            "🏢 Companies",
        ])
        with tabs[0]: tab_admin_overview(companies_df)
        with tabs[1]: tab_data_lab()
        with tabs[2]: tab_wrangling_lab()
        with tabs[3]: tab_eda()
        with tabs[4]: tab_ml_lab()
        with tabs[5]: tab_stats_lab()
        with tabs[6]: tab_companies(companies_df)

    st.markdown(
        '<hr style="border-color:#1f2937;">'
        '<div class="small-muted" style="text-align:center;padding:6px 0 18px 0;">'
        'FDA Placement Analytics · Built with Streamlit · '
        'NumPy · Pandas · Matplotlib · Seaborn · scikit-learn · SciPy'
        '</div>', unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
