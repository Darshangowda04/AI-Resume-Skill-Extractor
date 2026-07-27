import re
import streamlit as st
import pdfplumber
from docx import Document
import os
import matplotlib.pyplot as plt
SKILLS = [
        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Flask",
        "Django",
        "TensorFlow",
        "Keras",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Scikit-learn",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Computer Vision",
        "Git",
        "GitHub",
        "Docker",
        "AWS",
        "Azure",
        "Streamlit"
    ]
RECOMMENDED_SKILLS = [
        "Python",
        "SQL",
        "Git",
        "GitHub",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Pandas",
        "NumPy",
        "Streamlit"
    ]

st.set_page_config(
        page_title="Resume Skill Extractor",
        page_icon="📄",
        layout="wide"
    )

st.title("📄 Resume Skill Extractor")

st.write("Upload a PDF or DOCX resume to extract its text.")

uploaded_file = st.file_uploader(
    "Choose your Resume",
    type=["pdf", "docx"]
)

# ---------------- PDF -----------------
def extract_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ---------------- DOCX -----------------
def extract_docx(file):
    doc = Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):
    pattern = r"\+?\d[\d\s\-]{8,}\d"
    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_education(text):
    education_keywords = [
        "Bachelor",
        "B.E",
        "B.Tech",
        "BSc",
        "M.E",
        "M.Tech",
        "MSc",
        "MBA",
        "PhD",
        "Diploma",
        "PUC",
        "SSLC"
    ]

    education = []

    for line in text.split("\n"):
        for keyword in education_keywords:
            if keyword.lower() in line.lower():
                education.append(line.strip())

    return list(set(education))


def extract_name(text):
    lines = text.split("\n")

    for line in lines:
        if len(line.strip()) > 2:
            return line.strip()

    return "Not Found"


def extract_projects(text):
    projects = []
    lines = text.split("\n")

    capture = False

    stop_words = [
        "skills",
        "technical skills",
        "certificates",
        "certifications",
        "education",
        "languages",
        "achievements",
        "internship",
        "experience"
    ]

    for line in lines:
        line = line.strip()

        if "project" in line.lower():
            capture = True
            continue

        if capture:
            if any(word in line.lower() for word in stop_words):
                break

            if line != "":
                projects.append(line)

    return projects


def calculate_resume_score(skills, education, projects):
    score = 0

    # Skills (50 marks)
    score += min(len(skills) * 5, 50)

    # Education (20 marks)
    if education:
        score += 20

    # Projects (30 marks)
    score += min(len(projects) * 5, 30)

    return min(score, 100)


def missing_skills(skills):
    missing = []

    for skill in RECOMMENDED_SKILLS:
        if skill not in skills:
            missing.append(skill)

    return missing
def skill_match_percentage(skills):

    matched = len(set(skills) & set(RECOMMENDED_SKILLS))

    percentage = (matched / len(RECOMMENDED_SKILLS)) * 100

    return round(percentage, 2)

def predict_job_role(skills):
    job_roles = {
        "AI/ML Engineer": [
            "Python", "Machine Learning", "Deep Learning",
            "TensorFlow", "PyTorch", "Scikit-learn"
        ],

        "Data Scientist": [
            "Python", "Pandas", "NumPy",
            "SQL", "Machine Learning"
        ],

        "Data Analyst": [
            "SQL", "Excel", "Power BI",
            "Pandas", "Python"
        ],

        "Web Developer": [
            "HTML", "CSS", "JavaScript",
            "React", "Node.js", "Flask"
        ],

        "Python Developer": [
            "Python", "Flask", "Django",
            "Git"
        ]
    }

    best_role = "General Software Engineer"
    highest_score = 0

    for role, required_skills in job_roles.items():
        score = len(set(skills) & set(required_skills))

        if score > highest_score:
            highest_score = score
            best_role = role

    return best_role


# ---------------- Main -----------------
skills = []
education = []
projects = []
score = 0
missing = []
match = 0.0
job_role = "General Software Engineer"
resume_text = ""

if uploaded_file is not None:
    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "pdf":
        resume_text = extract_pdf(uploaded_file)

    elif extension == "docx":
        resume_text = extract_docx(uploaded_file)

    else:
        st.error("Unsupported File")

    st.success("Resume uploaded successfully!")

    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    projects = extract_projects(resume_text)
    score = calculate_resume_score(
        skills,
        education,
        projects
    )

    missing = missing_skills(skills)
    match = skill_match_percentage(skills)
    job_role = predict_job_role(skills)

    # Candidate Details
    st.subheader("Candidate Details")

    st.write("### 👤 Name")
    st.write(name)

    st.write("### 📧 Email")
    st.write(email)

    st.write("### 📱 Phone")
    st.write(phone)

    # Skills
    st.write("### 💻 Skills")

    if skills:
        for skill in skills:
            st.success(skill)
    else:
        st.warning("No skills detected")

    # Education
    st.write("### 🎓 Education")

    if education:
        for edu in education:
            st.success(edu)
    else:
        st.warning("Education not found")

    # Projects
    st.write("### 🚀 Projects")

    if projects:
        for project in projects:
            st.success(project)
    else:
        st.warning("Projects not found")

    # Resume Score
    st.subheader("📊 Resume Score")

    st.progress(score / 100)

    st.metric(
        label="Overall Resume Score",
        value=f"{score}/100"
    )

    st.subheader("🎯 Skill Match")
    st.progress(match / 100)
    st.metric(
        "Skill Match",
        f"{match}%"
    )

    st.subheader("💪 Resume Strengths")

    strengths = []

    if len(skills) >= 8:
        strengths.append("Good technical skill set")

    if education:
        strengths.append("Education details present")

    if len(projects) >= 3:
        strengths.append("Strong project portfolio")

    if score >= 90:
        strengths.append("Excellent ATS score")

    for strength in strengths:
        st.success(strength)

    st.subheader("📊 Skill Analytics")

    if skills:
        fig, ax = plt.subplots(figsize=(10, 4))
        values = [1] * len(skills)

        ax.bar(skills, values)
        ax.set_ylabel("Detected")
        ax.set_xlabel("Skills")
        ax.set_title("Detected Skills")
        plt.xticks(rotation=45)

        st.pyplot(fig)
    else:
        st.warning("No skills available for chart.")

    # Resume Feedback
    st.subheader("💡 Resume Feedback")

    if score >= 90:
        st.success("Excellent Resume! Ready for most job applications.")
    elif score >= 75:
        st.info("Good Resume. A few improvements can make it stronger.")
    elif score >= 50:
        st.warning("Average Resume. Add more skills, projects, or achievements.")
    else:
        st.error("Resume needs significant improvements.")

    # Missing Skills
    st.subheader("❌ Recommended Skills to Learn")

    if missing:
        for skill in missing:
            st.warning(skill)
    else:
        st.success("Your resume contains all recommended skills.")

    # Job Role
    st.subheader("🎯 Recommended Job Role")
    st.success(job_role)

    # Resume Text
    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "",
        resume_text,
        height=450
    )