# ============================================================================
# PLACEMENT READINESS & SKILL GAP ANALYTICS SYSTEM - ULTIMATE VERSION
# ============================================================================
# Academic Project: Foundations of Data Analytics (FDA)
# Version: 2.0 - ADMIN EDITION WITH FULL DATABASE MANAGEMENT
# Tech Stack: Streamlit, Pandas, NumPy, Matplotlib, Seaborn
# Type: Analytics Dashboard (Rule-based, No ML)
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Placement Analytics System - Ultimate Edition",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING - ENHANCED
# ============================================================================

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .admin-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #dc3545;
        text-align: center;
        padding: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .admin-badge {
        background-color: #dc3545;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    .student-badge {
        background-color: #28a745;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# ENHANCED USER DATABASE WITH ROLES AND PROFILES
# ============================================================================

USERS_DATABASE = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "System Administrator",
        "email": "admin@placement.edu"
    },
    "student": {
        "password": "1234",
        "role": "student",
        "name": "Student 1",
        "email": "student@university.edu",
        "cgpa": 7.5,
        "profile_data": {}
    },
    "student2": {
        "password": "pass123",
        "role": "student",
        "name": "Student 2",
        "email": "student2@university.edu",
        "cgpa": 8.2,
        "profile_data": {}
    },
    "alice_smith": {
        "password": "alice123",
        "role": "student",
        "name": "Alice",
        "email": "alice@university.edu",
        "cgpa": 8.8,
        "profile_data": {}
    },
    "bob_wilson": {
        "password": "bob123",
        "role": "student",
        "name": "Bob Wilson",
        "email": "bob@university.edu",
        "cgpa": 7.0,
        "profile_data": {}
    }
}

# ============================================================================
# ENHANCED COMPANY DATASET WITH MORE DETAILS
# ============================================================================

def load_company_dataset():
    """
    Creates a comprehensive company dataset with hiring criteria
    """
    companies_data = {
        "Company": [
            "Google", "Amazon", "Microsoft", "Apple", "Meta",
            "TCS", "Infosys", "Wipro", "Cognizant", "Accenture",
            "Adobe", "Oracle", "Salesforce", "IBM", "Capgemini",
            "HCL", "Tech Mahindra", "Flipkart", "Paytm", "Zomato",
            "Netflix", "Uber", "Airbnb", "Spotify", "LinkedIn"
        ],
        "Type": [
            "Product", "Product", "Product", "Product", "Product",
            "Service", "Service", "Service", "Service", "Service",
            "Product", "Product", "Product", "Service", "Service",
            "Service", "Service", "Product", "Product", "Product",
            "Product", "Product", "Product", "Product", "Product"
        ],
        "Min_CGPA": [
            8.5, 8.0, 8.2, 8.5, 8.3,
            6.5, 6.0, 6.2, 6.5, 6.8,
            8.0, 7.5, 7.8, 7.0, 6.5,
            6.0, 6.3, 7.5, 7.0, 6.8,
            8.0, 7.8, 8.2, 7.5, 8.0
        ],
        "Max_Backlogs": [
            0, 0, 0, 0, 0,
            2, 3, 2, 2, 1,
            0, 1, 1, 2, 2,
            3, 3, 1, 1, 2,
            0, 0, 0, 1, 0
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
            ["Python", "Payment Gateway", "Backend"],
            ["Python", "Backend Development", "Microservices"],
            ["DSA", "Python", "Microservices", "System Design"],
            ["DSA", "Go", "Distributed Systems", "Cloud"],
            ["DSA", "Python", "React", "Mobile Development"],
            ["DSA", "Python", "Audio Processing", "Cloud"],
            ["DSA", "Java", "Big Data", "System Design"]
        ],
        "Salary_LPA": [
            45, 42, 40, 48, 44,
            3.5, 4.0, 3.8, 4.2, 5.0,
            12, 10, 14, 8, 6,
            4.5, 5.5, 15, 12, 10,
            50, 38, 42, 35, 40
        ],
        "Job_Role": [
            "Software Engineer", "SDE", "Software Developer", "iOS Developer", "Software Engineer",
            "IT Analyst", "System Engineer", "Project Engineer", "Programmer Analyst", "Application Developer",
            "Software Engineer", "Associate Consultant", "Developer", "Application Developer", "Analyst",
            "Software Engineer", "Engineer", "Backend Developer", "Software Developer", "Backend Developer",
            "Senior Software Engineer", "Software Engineer", "Full Stack Developer", "Backend Engineer", "Software Engineer"
        ],
        "Location": [
            "Bangalore", "Bangalore", "Hyderabad", "Bangalore", "Bangalore",
            "Multiple Cities", "Bangalore", "Pune", "Chennai", "Bangalore",
            "Bangalore", "Bangalore", "Bangalore", "Multiple Cities", "Multiple Cities",
            "Noida", "Pune", "Bangalore", "Noida", "Gurgaon",
            "Mumbai", "Bangalore", "Bangalore", "Mumbai", "Bangalore"
        ],
        "Industry": [
            "Technology", "E-commerce", "Technology", "Technology", "Social Media",
            "IT Services", "IT Services", "IT Services", "IT Services", "Consulting",
            "Software", "Enterprise Software", "Cloud/CRM", "Technology", "Consulting",
            "IT Services", "Telecom", "E-commerce", "Fintech", "Food Tech",
            "Streaming", "Ride Sharing", "Travel Tech", "Music Streaming", "Professional Network"
        ],
        "Openings": [
            50, 80, 60, 30, 45,
            200, 250, 150, 180, 120,
            40, 50, 35, 100, 90,
            180, 140, 70, 60, 50,
            25, 45, 30, 28, 38
        ]
    }
    
    return pd.DataFrame(companies_data)

# ============================================================================
# SKILL CATEGORIES - EXPANDED
# ============================================================================

PROGRAMMING_LANGUAGES = [
    "Python", "Java", "C++", "C", "JavaScript", 
    "Go", "Rust", "Swift", "Kotlin", "R",
    "TypeScript", "Scala", "Ruby", "PHP", "Dart"
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
    "Distributed Systems", "Audio Processing", "Video Processing"
]

SOFT_SKILLS = [
    "Communication", "Teamwork", "Leadership", "Problem Solving",
    "Time Management", "Adaptability", "Critical Thinking",
    "Presentation Skills", "Interpersonal Skills", "Work Ethic",
    "Creativity", "Collaboration", "Decision Making"
]

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_role = ""
    st.session_state.analysis_done = False

# ============================================================================
# ANALYTICS DATA STORAGE (SIMULATED DATABASE)
# ============================================================================

if "student_analyses" not in st.session_state:
    st.session_state.student_analyses = []

if "placement_statistics" not in st.session_state:
    st.session_state.placement_statistics = {
        "total_students": 0,
        "total_analyses": 0,
        "avg_score": 0,
        "placement_rate": 0
    }

# ============================================================================
# CORE FUNCTIONS (SAME AS BEFORE BUT ENHANCED)
# ============================================================================

def calculate_employability_score(cgpa, backlogs, prog_langs, tech_skills, 
                                  soft_skills, certifications, internship, 
                                  company_alignment):
    """
    Rule-based employability score calculation
    """
    cgpa_score = (cgpa / 10.0) * 30
    total_skills = len(prog_langs) + len(tech_skills) + len(soft_skills)
    skills_score = min(total_skills / 20 * 25, 25)
    internship_score = 15 if internship else 0
    cert_score = min(certifications / 5 * 10, 10)
    alignment_score = min(company_alignment / 10 * 15, 15)
    backlogs_penalty = max(5 - backlogs * 1.5, 0)
    
    total_score = (cgpa_score + skills_score + internship_score + 
                   cert_score + alignment_score + backlogs_penalty)
    
    return round(total_score, 2)

def get_placement_probability(score):
    """
    Categorize placement probability based on employability score
    """
    if score >= 80:
        return "High (85-95%)", "success"
    elif score >= 60:
        return "Medium (55-75%)", "warning"
    elif score >= 40:
        return "Low (30-50%)", "warning"
    else:
        return "Very Low (<30%)", "danger"

def analyze_skill_gap(student_skills, company_skills):
    """
    Identify missing skills for a specific company
    """
    student_skill_set = set(student_skills)
    required_skill_set = set(company_skills)
    
    missing_skills = list(required_skill_set - student_skill_set)
    matching_skills = list(required_skill_set & student_skill_set)
    
    match_percentage = (len(matching_skills) / len(required_skill_set) * 100) if required_skill_set else 0
    
    return missing_skills, matching_skills, round(match_percentage, 2)

def generate_study_roadmap(missing_skills):
    """
    Generate personalized study plan for missing skills
    """
    skill_roadmap = {
        "DSA": {
            "duration": "8-12 weeks",
            "focus": "Arrays, Linked Lists, Trees, Graphs, DP",
            "resources": "LeetCode, GeeksforGeeks, Codeforces",
            "priority": "High"
        },
        "Python": {
            "duration": "4-6 weeks",
            "focus": "Syntax, OOP, Libraries (NumPy, Pandas)",
            "resources": "Python.org, Coursera, Udemy",
            "priority": "High"
        },
        "Java": {
            "duration": "6-8 weeks",
            "focus": "Core Java, Collections, Multithreading",
            "resources": "Oracle Docs, Java Point, Udemy",
            "priority": "High"
        },
        "System Design": {
            "duration": "6-8 weeks",
            "focus": "Scalability, Load Balancing, Databases",
            "resources": "System Design Primer, Gaurav Sen YouTube",
            "priority": "High"
        },
        "Cloud": {
            "duration": "4-6 weeks",
            "focus": "AWS/Azure basics, Cloud Computing concepts",
            "resources": "AWS Free Tier, Azure Learn",
            "priority": "Medium"
        },
        "AWS": {
            "duration": "5-7 weeks",
            "focus": "EC2, S3, Lambda, RDS",
            "resources": "AWS Training, A Cloud Guru",
            "priority": "Medium"
        },
        "SQL": {
            "duration": "3-4 weeks",
            "focus": "Queries, Joins, Indexing, Optimization",
            "resources": "W3Schools, SQLZoo, HackerRank",
            "priority": "High"
        },
        "React": {
            "duration": "5-6 weeks",
            "focus": "Components, Hooks, State Management",
            "resources": "React Official Docs, Scrimba",
            "priority": "Medium"
        },
        "Default": {
            "duration": "4-6 weeks",
            "focus": "Core concepts and practical implementation",
            "resources": "Online courses, YouTube tutorials, Documentation",
            "priority": "Medium"
        }
    }
    
    roadmap = []
    for skill in missing_skills:
        plan = skill_roadmap.get(skill, skill_roadmap["Default"])
        roadmap.append({
            "Skill": skill,
            "Priority": plan["priority"],
            "Duration": plan["duration"],
            "Focus Areas": plan["focus"],
            "Resources": plan["resources"]
        })
    
    return pd.DataFrame(roadmap)

def filter_eligible_companies(companies_df, cgpa, backlogs, student_skills):
    """
    Filter companies based on eligibility criteria
    """
    eligible = companies_df[
        (companies_df["Min_CGPA"] <= cgpa) & 
        (companies_df["Max_Backlogs"] >= backlogs)
    ].copy()
    
    skill_matches = []
    for _, company in eligible.iterrows():
        _, _, match_pct = analyze_skill_gap(student_skills, company["Required_Skills"])
        skill_matches.append(match_pct)
    
    eligible["Skill_Match_%"] = skill_matches
    eligible = eligible.sort_values("Skill_Match_%", ascending=False)
    
    return eligible

def get_career_recommendation(score, cgpa, skill_count):
    """
    Provide career path recommendation
    """
    if score >= 75 and cgpa >= 8.0:
        return "Product Company Ready", "You have strong potential for top product companies", "success"
    elif score >= 60 and cgpa >= 7.0:
        return "Service Company Ready", "Well-suited for reputed service companies", "warning"
    elif score >= 40:
        return "Needs Improvement", "Focus on building skills and improving CGPA", "warning"
    else:
        return "Critical Improvement Required", "Immediate action needed on multiple fronts", "danger"

def analyze_strengths_weaknesses(cgpa, backlogs, prog_langs, tech_skills, 
                                 soft_skills, certifications, internship):
    """
    Identify student strengths and areas of improvement
    """
    strengths = []
    weaknesses = []
    
    if cgpa >= 8.5:
        strengths.append("Excellent academic performance (CGPA: {})".format(cgpa))
    elif cgpa >= 7.0:
        strengths.append("Good academic performance (CGPA: {})".format(cgpa))
    else:
        weaknesses.append("Low CGPA ({}) - Needs improvement".format(cgpa))
    
    if backlogs == 0:
        strengths.append("No backlogs - Clean academic record")
    else:
        weaknesses.append("{} backlog(s) - Clear them soon".format(backlogs))
    
    total_skills = len(prog_langs) + len(tech_skills)
    if total_skills >= 10:
        strengths.append("Strong skill set ({} technical skills)".format(total_skills))
    elif total_skills >= 5:
        strengths.append("Decent skill set ({} technical skills)".format(total_skills))
    else:
        weaknesses.append("Limited skills ({}) - Learn more technologies".format(total_skills))
    
    if len(prog_langs) >= 3:
        strengths.append("Proficient in multiple programming languages")
    elif len(prog_langs) == 0:
        weaknesses.append("No programming language selected - Critical gap")
    
    if "DSA" in tech_skills:
        strengths.append("DSA knowledge - Essential for interviews")
    else:
        weaknesses.append("Missing DSA - Must learn for placements")
    
    if internship:
        strengths.append("Industry experience through internship")
    else:
        weaknesses.append("No internship experience - Try to get one")
    
    if certifications >= 3:
        strengths.append("{} certifications - Shows commitment".format(certifications))
    elif certifications == 0:
        weaknesses.append("No certifications - Consider getting some")
    
    if len(soft_skills) >= 5:
        strengths.append("Well-developed soft skills")
    else:
        weaknesses.append("Limited soft skills - Important for interviews")
    
    return strengths, weaknesses

def save_student_analysis(username, data):
    """
    Save student analysis to session state (simulated database)
    """
    analysis_record = {
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cgpa": data.get("cgpa"),
        "score": data.get("score"),
        "eligible_companies": data.get("eligible_companies"),
        "skills_count": data.get("skills_count"),
        "backlogs": data.get("backlogs"),
        "internship": data.get("internship"),
        "certifications": data.get("certifications")
    }
    
    st.session_state.student_analyses.append(analysis_record)

# ============================================================================
# VISUALIZATION FUNCTIONS - ENHANCED
# ============================================================================

def plot_cgpa_cutoffs(eligible_companies):
    """Bar chart showing CGPA cutoffs"""
    fig, ax = plt.subplots(figsize=(10, 6))
    companies = eligible_companies["Company"]
    cgpa_cutoffs = eligible_companies["Min_CGPA"]
    colors = ['#1f77b4' if t == 'Product' else '#ff7f0e' for t in eligible_companies["Type"]]
    
    ax.barh(companies, cgpa_cutoffs, color=colors)
    ax.set_xlabel("Minimum CGPA", fontsize=12, fontweight='bold')
    ax.set_ylabel("Company", fontsize=12, fontweight='bold')
    ax.set_title("CGPA Cutoffs of Eligible Companies", fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#1f77b4', label='Product'), Patch(facecolor='#ff7f0e', label='Service')]
    ax.legend(handles=legend_elements, loc='lower right')
    plt.tight_layout()
    return fig

def plot_skill_distribution(prog_langs, tech_skills, soft_skills):
    """Pie chart showing skill distribution"""
    fig, ax = plt.subplots(figsize=(8, 8))
    skill_counts = [len(prog_langs), len(tech_skills), len(soft_skills)]
    labels = ['Programming Languages', 'Technical Skills', 'Soft Skills']
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.05, 0.05, 0.05)
    
    ax.pie(skill_counts, labels=labels, autopct='%1.1f%%', startangle=90,
           colors=colors, explode=explode, shadow=True)
    ax.set_title("Your Skill Distribution", fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_salary_distribution(eligible_companies):
    """Histogram showing salary distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    salaries = eligible_companies["Salary_LPA"]
    
    ax.hist(salaries, bins=10, color='#2ca02c', edgecolor='black', alpha=0.7)
    ax.set_xlabel("Salary (LPA)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Number of Companies", fontsize=12, fontweight='bold')
    ax.set_title("Salary Distribution of Eligible Companies", fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig

def plot_company_type_distribution(eligible_companies):
    """Pie chart for product vs service"""
    fig, ax = plt.subplots(figsize=(8, 8))
    type_counts = eligible_companies["Type"].value_counts()
    colors = ['#1f77b4', '#ff7f0e']
    explode = (0.05, 0.05) if len(type_counts) > 1 else (0.05,)
    
    ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
           startangle=90, colors=colors[:len(type_counts)], explode=explode, shadow=True)
    ax.set_title("Product vs Service Companies (Eligible)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_skill_match_comparison(eligible_companies):
    """Bar chart for skill match percentages"""
    fig, ax = plt.subplots(figsize=(10, 6))
    top_companies = eligible_companies.head(10)
    companies = top_companies["Company"]
    match_percentages = top_companies["Skill_Match_%"]
    colors = ['#2ca02c' if m >= 70 else '#ffa500' if m >= 50 else '#d62728' for m in match_percentages]
    
    ax.barh(companies, match_percentages, color=colors)
    ax.set_xlabel("Skill Match %", fontsize=12, fontweight='bold')
    ax.set_ylabel("Company", fontsize=12, fontweight='bold')
    ax.set_title("Top 10 Companies by Skill Match", fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    return fig

# ADMIN VISUALIZATIONS

def plot_admin_score_distribution():
    """Admin: Overall score distribution"""
    if not st.session_state.student_analyses:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    scores = [a['score'] for a in st.session_state.student_analyses]
    
    ax.hist(scores, bins=15, color='#9b59b6', edgecolor='black', alpha=0.7)
    ax.set_xlabel("Employability Score", fontsize=12, fontweight='bold')
    ax.set_ylabel("Number of Students", fontsize=12, fontweight='bold')
    ax.set_title("Student Score Distribution", fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig

def plot_admin_cgpa_distribution():
    """Admin: CGPA distribution"""
    if not st.session_state.student_analyses:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cgpas = [a['cgpa'] for a in st.session_state.student_analyses]
    
    ax.hist(cgpas, bins=10, color='#3498db', edgecolor='black', alpha=0.7)
    ax.set_xlabel("CGPA", fontsize=12, fontweight='bold')
    ax.set_ylabel("Number of Students", fontsize=12, fontweight='bold')
    ax.set_title("CGPA Distribution", fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig

def plot_company_popularity(companies_df):
    """Admin: Most sought-after companies"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    top_20 = companies_df.nlargest(20, 'Salary_LPA')
    
    ax.barh(top_20['Company'], top_20['Salary_LPA'], color='#e74c3c')
    ax.set_xlabel("Salary (LPA)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Company", fontsize=12, fontweight='bold')
    ax.set_title("Top 20 Companies by Salary Package", fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    return fig

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    """User authentication page"""
    st.markdown('<p class="main-header">🎓 Placement Analytics System - Ultimate Edition</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login Portal")
        st.info("📚 Academic FDA Project - Enhanced with Admin Controls")
        
        st.markdown("#### 👨‍🎓 Student Credentials")
        st.code("Username: student | Password: 1234")
        st.code("Username: student2 | Password: pass123")
        
        st.markdown("#### 🔑 Admin Access")
        st.code("Username: admin | Password: admin123")
        
        st.markdown("---")
        
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
        
        if st.button("🚀 Login", use_container_width=True):
            if username in USERS_DATABASE and USERS_DATABASE[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = USERS_DATABASE[username]["role"]
                
                if st.session_state.user_role == "admin":
                    st.success(f"✅ Admin Access Granted! Welcome, {USERS_DATABASE[username]['name']}")
                else:
                    st.success(f"✅ Welcome, {USERS_DATABASE[username]['name']}!")
                
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        
        st.markdown("---")
        st.caption("🔒 Secure Authentication | 👨‍💼 Admin Dashboard Available")

# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

def admin_dashboard():
    """Complete admin control panel"""
    st.markdown('<p class="admin-header">👨‍💼 ADMIN CONTROL PANEL</p>', unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'><span class='admin-badge'>ADMIN MODE</span></div>", unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("## 🎛️ Admin Navigation")
    admin_section = st.sidebar.radio(
        "Select Section",
        ["📊 Dashboard Overview", "🏢 Company Database", "👥 Student Management", 
         "📈 Analytics & Reports", "⚙️ System Settings"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.rerun()
    
    companies_df = load_company_dataset()
    
    # ========================================================================
    # SECTION 1: DASHBOARD OVERVIEW
    # ========================================================================
    if admin_section == "📊 Dashboard Overview":
        st.markdown("---")
        st.markdown("## 📊 System Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Companies", len(companies_df), delta="Active")
        
        with col2:
            product_count = len(companies_df[companies_df["Type"] == "Product"])
            st.metric("Product Companies", product_count)
        
        with col3:
            service_count = len(companies_df[companies_df["Type"] == "Service"])
            st.metric("Service Companies", service_count)
        
        with col4:
            total_openings = companies_df["Openings"].sum()
            st.metric("Total Job Openings", total_openings)
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_students = len([u for u in USERS_DATABASE if USERS_DATABASE[u]["role"] == "student"])
            st.metric("Registered Students", total_students)
        
        with col2:
            total_analyses = len(st.session_state.student_analyses)
            st.metric("Total Analyses", total_analyses)
        
        with col3:
            if st.session_state.student_analyses:
                avg_score = sum([a['score'] for a in st.session_state.student_analyses]) / len(st.session_state.student_analyses)
                st.metric("Average Score", f"{avg_score:.2f}")
            else:
                st.metric("Average Score", "N/A")
        
        with col4:
            if st.session_state.student_analyses:
                high_scorers = len([a for a in st.session_state.student_analyses if a['score'] >= 80])
                placement_rate = (high_scorers / len(st.session_state.student_analyses)) * 100
                st.metric("High Scorers %", f"{placement_rate:.1f}%")
            else:
                st.metric("High Scorers %", "N/A")
        
        st.markdown("---")
        st.markdown("## 📈 Quick Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Salary Statistics")
            st.write(f"**Highest Package:** ₹{companies_df['Salary_LPA'].max()} LPA")
            st.write(f"**Average Package:** ₹{companies_df['Salary_LPA'].mean():.2f} LPA")
            st.write(f"**Median Package:** ₹{companies_df['Salary_LPA'].median()} LPA")
            st.write(f"**Lowest Package:** ₹{companies_df['Salary_LPA'].min()} LPA")
        
        with col2:
            st.markdown("### 🎯 Eligibility Criteria")
            st.write(f"**Highest CGPA Cutoff:** {companies_df['Min_CGPA'].max()}")
            st.write(f"**Average CGPA Cutoff:** {companies_df['Min_CGPA'].mean():.2f}")
            st.write(f"**Companies with 0 Backlogs:** {len(companies_df[companies_df['Max_Backlogs'] == 0])}")
            st.write(f"**Companies allowing Backlogs:** {len(companies_df[companies_df['Max_Backlogs'] > 0])}")
        
        st.markdown("---")
        st.markdown("## 📊 Visual Analytics")
        
        tab1, tab2 = st.tabs(["Company Analytics", "Student Analytics"])
        
        with tab1:
            st.pyplot(plot_company_popularity(companies_df))
            
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(8, 8))
                type_counts = companies_df["Type"].value_counts()
                ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
                ax.set_title("Company Type Distribution", fontweight='bold')
                st.pyplot(fig)
            
            with col2:
                fig, ax = plt.subplots(figsize=(8, 8))
                location_counts = companies_df["Location"].value_counts().head(10)
                ax.pie(location_counts.values, labels=location_counts.index, autopct='%1.1f%%', startangle=90)
                ax.set_title("Top 10 Locations", fontweight='bold')
                st.pyplot(fig)
        
        with tab2:
            if st.session_state.student_analyses:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = plot_admin_score_distribution()
                    if fig:
                        st.pyplot(fig)
                
                with col2:
                    fig = plot_admin_cgpa_distribution()
                    if fig:
                        st.pyplot(fig)
            else:
                st.info("No student analysis data available yet")
    
    # ========================================================================
    # SECTION 2: COMPANY DATABASE
    # ========================================================================
    elif admin_section == "🏢 Company Database":
        st.markdown("---")
        st.markdown("## 🏢 Complete Company Database")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.multiselect("Filter by Type", ["Product", "Service"], default=["Product", "Service"])
        
        with col2:
            min_salary = st.slider("Minimum Salary (LPA)", 0, 50, 0)
        
        with col3:
            filter_location = st.multiselect("Filter by Location", companies_df["Location"].unique().tolist())
        
        # Apply filters
        filtered_df = companies_df[companies_df["Type"].isin(filter_type)]
        filtered_df = filtered_df[filtered_df["Salary_LPA"] >= min_salary]
        
        if filter_location:
            filtered_df = filtered_df[filtered_df["Location"].isin(filter_location)]
        
        st.markdown(f"### Showing {len(filtered_df)} companies")
        
        # Display full database
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=500
        )
        
        # Download option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Company Database (CSV)",
            data=csv,
            file_name="company_database.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.markdown("## 🔍 Detailed Company View")
        
        selected_company = st.selectbox("Select a company for details", filtered_df["Company"].tolist())
        
        if selected_company:
            company_info = filtered_df[filtered_df["Company"] == selected_company].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📋 Basic Information")
                st.write(f"**Company:** {company_info['Company']}")
                st.write(f"**Type:** {company_info['Type']}")
                st.write(f"**Industry:** {company_info['Industry']}")
                st.write(f"**Location:** {company_info['Location']}")
                st.write(f"**Job Role:** {company_info['Job_Role']}")
                st.write(f"**Openings:** {company_info['Openings']}")
            
            with col2:
                st.markdown("### 🎯 Eligibility Criteria")
                st.write(f"**Minimum CGPA:** {company_info['Min_CGPA']}")
                st.write(f"**Max Backlogs Allowed:** {company_info['Max_Backlogs']}")
                st.write(f"**Salary Package:** ₹{company_info['Salary_LPA']} LPA")
                
                st.markdown("### 🛠️ Required Skills")
                for skill in company_info['Required_Skills']:
                    st.success(f"✓ {skill}")
        
        st.markdown("---")
        st.markdown("## 📊 Company Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Top 5 by Salary")
            top_salary = filtered_df.nlargest(5, 'Salary_LPA')[['Company', 'Salary_LPA']]
            st.dataframe(top_salary, use_container_width=True)
        
        with col2:
            st.markdown("### Most Openings")
            top_openings = filtered_df.nlargest(5, 'Openings')[['Company', 'Openings']]
            st.dataframe(top_openings, use_container_width=True)
        
        with col3:
            st.markdown("### Easiest to Get")
            easiest = filtered_df.nsmallest(5, 'Min_CGPA')[['Company', 'Min_CGPA']]
            st.dataframe(easiest, use_container_width=True)
    
    # ========================================================================
    # SECTION 3: STUDENT MANAGEMENT
    # ========================================================================
    elif admin_section == "👥 Student Management":
        st.markdown("---")
        st.markdown("## 👥 Student Database")
        
        # Create student dataframe
        students = []
        for username, data in USERS_DATABASE.items():
            if data["role"] == "student":
                students.append({
                    "Username": username,
                    "Name": data["name"],
                    "Email": data["email"],
                    "CGPA": data.get("cgpa", "N/A")
                })
        
        students_df = pd.DataFrame(students)
        
        st.dataframe(students_df, use_container_width=True)
        
        st.markdown("---")
        st.markdown("## 📊 Student Analysis Records")
        
        if st.session_state.student_analyses:
            analyses_df = pd.DataFrame(st.session_state.student_analyses)
            
            st.dataframe(analyses_df, use_container_width=True, height=400)
            
            # Download
            csv = analyses_df.to_csv(index=False)
            st.download_button(
                label="📥 Download All Student Analyses",
                data=csv,
                file_name="student_analyses.csv",
                mime="text/csv"
            )
            
            st.markdown("---")
            st.markdown("## 🔍 Individual Student Details")
            
            usernames = list(set([a['username'] for a in st.session_state.student_analyses]))
            selected_student = st.selectbox("Select Student", usernames)
            
            if selected_student:
                student_data = [a for a in st.session_state.student_analyses if a['username'] == selected_student]
                
                st.markdown(f"### Analysis History for {selected_student}")
                st.write(f"**Total Analyses:** {len(student_data)}")
                
                if student_data:
                    latest = student_data[-1]
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Latest Score", latest['score'])
                    
                    with col2:
                        st.metric("CGPA", latest['cgpa'])
                    
                    with col3:
                        st.metric("Skills", latest['skills_count'])
                    
                    with col4:
                        st.metric("Eligible Companies", latest['eligible_companies'])
                    
                    st.markdown("### Analysis Timeline")
                    timeline_df = pd.DataFrame(student_data)
                    st.dataframe(timeline_df, use_container_width=True)
        else:
            st.info("No student analyses recorded yet")
    
    # ========================================================================
    # SECTION 4: ANALYTICS & REPORTS
    # ========================================================================
    elif admin_section == "📈 Analytics & Reports":
        st.markdown("---")
        st.markdown("## 📈 Comprehensive Analytics")
        
        tab1, tab2, tab3 = st.tabs(["Company Analytics", "Student Performance", "Trends & Insights"])
        
        with tab1:
            st.markdown("### 🏢 Company-wise Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Industry Distribution")
                industry_counts = companies_df["Industry"].value_counts()
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(industry_counts.index, industry_counts.values, color='#3498db')
                ax.set_xlabel("Industry")
                ax.set_ylabel("Number of Companies")
                ax.set_title("Companies by Industry")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
            
            with col2:
                st.markdown("#### Salary vs CGPA Cutoff")
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(companies_df['Min_CGPA'], companies_df['Salary_LPA'], 
                                   c=companies_df['Type'].map({'Product': 1, 'Service': 0}),
                                   cmap='viridis', s=100, alpha=0.6)
                ax.set_xlabel("Minimum CGPA")
                ax.set_ylabel("Salary (LPA)")
                ax.set_title("Salary vs CGPA Requirements")
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
            
            st.markdown("#### Job Openings by Company")
            top_openings = companies_df.nlargest(15, 'Openings')
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.barh(top_openings['Company'], top_openings['Openings'], color='#e74c3c')
            ax.set_xlabel("Number of Openings")
            ax.set_ylabel("Company")
            ax.set_title("Top 15 Companies by Job Openings")
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab2:
            if st.session_state.student_analyses:
                st.markdown("### 👨‍🎓 Student Performance Metrics")
                
                analyses_df = pd.DataFrame(st.session_state.student_analyses)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_score = analyses_df['score'].mean()
                    st.metric("Average Employability Score", f"{avg_score:.2f}")
                
                with col2:
                    avg_cgpa = analyses_df['cgpa'].mean()
                    st.metric("Average CGPA", f"{avg_cgpa:.2f}")
                
                with col3:
                    avg_skills = analyses_df['skills_count'].mean()
                    st.metric("Average Skills per Student", f"{avg_skills:.1f}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Score Distribution")
                    fig = plot_admin_score_distribution()
                    if fig:
                        st.pyplot(fig)
                
                with col2:
                    st.markdown("#### CGPA Distribution")
                    fig = plot_admin_cgpa_distribution()
                    if fig:
                        st.pyplot(fig)
                
                st.markdown("#### Performance Categories")
                
                high = len(analyses_df[analyses_df['score'] >= 80])
                medium = len(analyses_df[(analyses_df['score'] >= 60) & (analyses_df['score'] < 80)])
                low = len(analyses_df[analyses_df['score'] < 60])
                
                fig, ax = plt.subplots(figsize=(8, 8))
                sizes = [high, medium, low]
                labels = ['High (≥80)', 'Medium (60-79)', 'Low (<60)']
                colors = ['#2ecc71', '#f39c12', '#e74c3c']
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
                ax.set_title("Student Performance Categories")
                st.pyplot(fig)
            else:
                st.info("No student data available yet")
        
        with tab3:
            st.markdown("### 📊 Trends & Insights")
            
            st.markdown("#### Key Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success("**Top Paying Industries**")
                top_industries = companies_df.groupby('Industry')['Salary_LPA'].mean().sort_values(ascending=False).head(5)
                for industry, salary in top_industries.items():
                    st.write(f"• {industry}: ₹{salary:.2f} LPA")
            
            with col2:
                st.info("**Most Accessible Companies**")
                accessible = companies_df.nsmallest(5, 'Min_CGPA')[['Company', 'Min_CGPA', 'Max_Backlogs']]
                st.dataframe(accessible, use_container_width=True)
            
            st.markdown("#### Skill Demand Analysis")
            
            all_skills = []
            for skills_list in companies_df['Required_Skills']:
                all_skills.extend(skills_list)
            
            skill_counts = pd.Series(all_skills).value_counts().head(15)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.barh(skill_counts.index, skill_counts.values, color='#9b59b6')
            ax.set_xlabel("Frequency")
            ax.set_ylabel("Skill")
            ax.set_title("Top 15 Most Demanded Skills Across Companies")
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
    
    # ========================================================================
    # SECTION 5: SYSTEM SETTINGS
    # ========================================================================
    elif admin_section == "⚙️ System Settings":
        st.markdown("---")
        st.markdown("## ⚙️ System Configuration")
        
        st.markdown("### 📊 Database Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", len(USERS_DATABASE))
            st.metric("Student Accounts", len([u for u in USERS_DATABASE if USERS_DATABASE[u]["role"] == "student"]))
            st.metric("Admin Accounts", len([u for u in USERS_DATABASE if USERS_DATABASE[u]["role"] == "admin"]))
        
        with col2:
            st.metric("Total Companies", len(companies_df))
            st.metric("Total Skills Tracked", len(PROGRAMMING_LANGUAGES) + len(TECHNICAL_SKILLS) + len(SOFT_SKILLS))
            st.metric("Analysis Records", len(st.session_state.student_analyses))
        
        with col3:
            if st.session_state.student_analyses:
                st.metric("Data Since", st.session_state.student_analyses[0]['timestamp'][:10])
            else:
                st.metric("Data Since", "N/A")
        
        st.markdown("---")
        st.markdown("### 🗄️ Database Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export All Data", use_container_width=True):
                # Export companies
                companies_csv = companies_df.to_csv(index=False)
                
                st.download_button(
                    label="Download Company Database",
                    data=companies_csv,
                    file_name="companies_export.csv",
                    mime="text/csv"
                )
                
                st.success("✅ Export ready!")
        
        with col2:
            if st.button("🧹 Clear Analysis Data", use_container_width=True, type="secondary"):
                if st.checkbox("Confirm clear all student analyses"):
                    st.session_state.student_analyses = []
                    st.success("✅ Analysis data cleared")
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 System Information")
        
        st.info(f"""
        **System Version:** 2.0 Ultimate Edition  
        **Last Updated:** {datetime.now().strftime("%Y-%m-%d")}  
        **Features:** Admin Dashboard, Database Management, Analytics Engine  
        **Status:** ✅ Fully Operational
        """)

# ============================================================================
# STUDENT DASHBOARD (ENHANCED VERSION)
# ============================================================================

def student_dashboard():
    """Student analytics dashboard"""
    st.markdown(f'<p class="main-header">🎓 Placement Readiness Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'><span class='student-badge'>STUDENT MODE</span></div>", unsafe_allow_html=True)
    st.markdown(f"**Logged in as:** {st.session_state.username}")
    
    companies_df = load_company_dataset()
    
    # Sidebar
    st.sidebar.markdown("## 📋 Student Profile")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 📚 Academic Details")
    cgpa = st.sidebar.slider("CGPA", 0.0, 10.0, 7.5, 0.1)
    backlogs = st.sidebar.number_input("Current Backlogs", 0, 10, 0)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 💻 Programming Languages")
    prog_langs = st.sidebar.multiselect("Select languages", PROGRAMMING_LANGUAGES)
    
    st.sidebar.markdown("### 🛠️ Technical Skills")
    tech_skills = st.sidebar.multiselect("Select technical skills", TECHNICAL_SKILLS)
    
    st.sidebar.markdown("### 🤝 Soft Skills")
    soft_skills = st.sidebar.multiselect("Select soft skills", SOFT_SKILLS)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 📜 Additional Information")
    certifications = st.sidebar.number_input("Certifications", 0, 20, 0)
    internship = st.sidebar.radio("Internship Experience", ["No", "Yes"]) == "Yes"
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 🎯 Preferences")
    company_preference = st.sidebar.selectbox("Preferred Type", ["Any", "Product", "Service"])
    
    st.sidebar.markdown("---")
    
    analyze_button = st.sidebar.button("🔍 Analyze Profile", use_container_width=True)
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.rerun()
    
    # Main content
    if analyze_button:
        if not prog_langs and not tech_skills:
            st.error("⚠️ Please select at least some skills!")
            return
        
        all_student_skills = prog_langs + tech_skills
        
        all_required_skills = []
        for skills_list in companies_df["Required_Skills"]:
            all_required_skills.extend(skills_list)
        
        unique_required = set(all_required_skills)
        student_skill_set = set(all_student_skills)
        company_alignment = len(unique_required & student_skill_set)
        
        emp_score = calculate_employability_score(
            cgpa, backlogs, prog_langs, tech_skills, soft_skills,
            certifications, internship, company_alignment
        )
        
        prob_text, prob_status = get_placement_probability(emp_score)
        career_path, career_desc, career_status = get_career_recommendation(emp_score, cgpa, len(all_student_skills))
        strengths, weaknesses = analyze_strengths_weaknesses(
            cgpa, backlogs, prog_langs, tech_skills, soft_skills, certifications, internship
        )
        
        # Save analysis
        save_student_analysis(st.session_state.username, {
            "cgpa": cgpa,
            "score": emp_score,
            "eligible_companies": 0,  # Will update
            "skills_count": len(all_student_skills),
            "backlogs": backlogs,
            "internship": internship,
            "certifications": certifications
        })
        
        # Overview
        st.markdown("---")
        st.markdown('<p class="sub-header">📊 Profile Overview</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Employability Score", f"{emp_score}/100")
        with col2:
            st.metric("CGPA", f"{cgpa}/10.0")
        with col3:
            st.metric("Total Skills", len(all_student_skills))
        with col4:
            st.metric("Backlogs", backlogs)
        
        st.markdown("---")
        
        # Placement Analysis
        st.markdown('<p class="sub-header">🎯 Placement Analysis</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if prob_status == "success":
                st.success(f"**Placement Probability:** {prob_text}")
            else:
                st.warning(f"**Placement Probability:** {prob_text}")
        
        with col2:
            if career_status == "success":
                st.success(f"**Career Path:** {career_path}")
            else:
                st.warning(f"**Career Path:** {career_path}")
        
        st.info(f"💡 **Recommendation:** {career_desc}")
        
        st.markdown("---")
        
        # Strengths & Weaknesses
        st.markdown('<p class="sub-header">⚡ Strengths & Areas of Improvement</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Your Strengths")
            for strength in strengths:
                st.markdown(f"- {strength}")
        
        with col2:
            st.markdown("#### ⚠️ Areas to Improve")
            for weakness in weaknesses:
                st.markdown(f"- {weakness}")
        
        st.markdown("---")
        
        # Eligible Companies
        st.markdown('<p class="sub-header">🏢 Eligible Companies</p>', unsafe_allow_html=True)
        
        filtered_companies = companies_df.copy()
        if company_preference != "Any":
            filtered_companies = filtered_companies[filtered_companies["Type"] == company_preference]
        
        eligible_companies = filter_eligible_companies(filtered_companies, cgpa, backlogs, all_student_skills)
        
        # Update saved analysis
        st.session_state.student_analyses[-1]['eligible_companies'] = len(eligible_companies)
        
        if not eligible_companies.empty:
            st.success(f"✅ You are eligible for **{len(eligible_companies)}** companies!")
            
            display_df = eligible_companies[['Company', 'Type', 'Min_CGPA', 'Skill_Match_%', 'Salary_LPA', 'Job_Role']].head(10)
            st.dataframe(display_df, use_container_width=True, height=400)
            
            csv = eligible_companies.to_csv(index=False)
            st.download_button(
                label="📥 Download Full List",
                data=csv,
                file_name=f"eligible_companies_{st.session_state.username}.csv",
                mime="text/csv"
            )
        else:
            st.error("❌ No companies match your profile")
        
        st.markdown("---")
        
        # Skill Gap Analysis
        if not eligible_companies.empty:
            st.markdown('<p class="sub-header">🔍 Skill Gap Analysis</p>', unsafe_allow_html=True)
            
            selected_company = st.selectbox("Select company", eligible_companies["Company"].tolist())
            
            company_data = eligible_companies[eligible_companies["Company"] == selected_company].iloc[0]
            missing, matching, match_pct = analyze_skill_gap(all_student_skills, company_data["Required_Skills"])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Required", len(company_data["Required_Skills"]))
            with col2:
                st.metric("Matching", len(matching))
            with col3:
                st.metric("Match %", f"{match_pct}%")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ✅ Skills You Have")
                for skill in matching:
                    st.success(f"✓ {skill}")
            
            with col2:
                st.markdown("#### ❌ Skills You Need")
                for skill in missing:
                    st.error(f"✗ {skill}")
            
            # Study Roadmap
            if missing:
                st.markdown("---")
                st.markdown('<p class="sub-header">📚 Study Roadmap</p>', unsafe_allow_html=True)
                
                roadmap_df = generate_study_roadmap(missing)
                st.dataframe(roadmap_df, use_container_width=True, height=300)
                
                roadmap_csv = roadmap_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Roadmap",
                    data=roadmap_csv,
                    file_name=f"roadmap_{selected_company}.csv",
                    mime="text/csv"
                )
        
        st.markdown("---")
        
        # Visualizations
        st.markdown('<p class="sub-header">📈 Visual Analytics</p>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 CGPA", "🥧 Skills", "💰 Salary", "🏢 Types", "🎯 Matching"
        ])
        
        with tab1:
            if not eligible_companies.empty:
                st.pyplot(plot_cgpa_cutoffs(eligible_companies.head(15)))
        
        with tab2:
            if prog_langs or tech_skills or soft_skills:
                st.pyplot(plot_skill_distribution(prog_langs, tech_skills, soft_skills))
        
        with tab3:
            if not eligible_companies.empty:
                st.pyplot(plot_salary_distribution(eligible_companies))
        
        with tab4:
            if not eligible_companies.empty:
                st.pyplot(plot_company_type_distribution(eligible_companies))
        
        with tab5:
            if not eligible_companies.empty and len(eligible_companies) >= 5:
                st.pyplot(plot_skill_match_comparison(eligible_companies))
        
        st.markdown("---")
        
        # Final Recommendations
        st.markdown('<p class="sub-header">💡 Final Recommendations</p>', unsafe_allow_html=True)
        
        if emp_score >= 75:
            st.success("**🎉 Excellent!** Strong profile for top companies")
        elif emp_score >= 60:
            st.info("**👍 Good!** Decent chances, work on gaps")
        else:
            st.warning("**⚠️ Needs Work!** Focus on improvement areas")
        
        st.success("✅ Analysis Complete!")
    
    else:
        # Welcome screen
        st.markdown("---")
        st.info("""
        ### 👋 Welcome!
        
        Fill your profile in the sidebar and click **"Analyze Profile"** to:
        - ✅ Get your employability score
        - 📊 Find eligible companies
        - 🔍 Analyze skill gaps
        - 📚 Get study roadmaps
        - 📈 View analytics
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Companies", len(companies_df))
        with col2:
            st.metric("Product", len(companies_df[companies_df["Type"] == "Product"]))
        with col3:
            st.metric("Service", len(companies_df[companies_df["Type"] == "Service"]))
        with col4:
            st.metric("Skills", len(PROGRAMMING_LANGUAGES) + len(TECHNICAL_SKILLS))
    
    st.markdown("---")
    st.caption("🎓 Placement Analytics System - Ultimate Edition | Built with Streamlit")

# ============================================================================
# MAIN APPLICATION CONTROLLER
# ============================================================================

def main():
    """Main application router"""
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_role == "admin":
            admin_dashboard()
        else:
            student_dashboard()

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
