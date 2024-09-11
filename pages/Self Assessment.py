import cohere
import streamlit as st
import PyPDF2
from docx import Document

# Initialize Cohere client
co = cohere.Client('GHyObF1CtNtzlgdHzrpdnXVq8lZRjporWOnGWo3Y')

# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    text = ""
    try:
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX file: {e}")
    return text

# Function to extract skills from resume using the correct API method
def extract_skills_from_resume(resume_text):
    prompt = f"""
    Extract skills from the following resume text.

    Resume: {resume_text}
    Skills: """

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
    )
  
    return response.generations[0].text.replace("Skills: ", "").split(',')

# Functions to find skill gaps, recommend courses, and recommend jobs
def find_skill_gaps(profile_summary, skills_ratings):
    prompt = f"""
    Given the candidate's profile and the skills they rated, find the skills they need to improve and recommend additional skills.

    Profile: {profile_summary}
    Skills Ratings: {', '.join([f"{skill} ({rating}/10)" for skill, rating in skills_ratings.items()])}
    Suggested Improvements: """

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
  
    return response.generations[0].text.replace("Suggested Improvements: ", "").split(',')

def recommend_courses(missing_skills):
    prompt = f"""
    Recommend online courses for the following skills.

    Skills: {', '.join(missing_skills)}
    Courses: """

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
  
    return response.generations[0].text.replace("Courses: ", "").split(',')

def recommend_jobs(profile_summary):
    prompt = f"""
    Based on the candidate's profile, recommend job titles they should consider.

    Profile: {profile_summary}
    Recommended Jobs: """

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
  
    return response.generations[0].text.replace("Recommended Jobs: ", "").split(',')

# Function to compare user's skills against required skills for a job role
def compare_skills_with_job_role(user_skills, job_role):
    prompt = f"""
    Based on the job role '{job_role}', list the key skills required for the role.
    
    Job Role: {job_role}
    Required Skills: """

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
  
    required_skills = response.generations[0].text.replace("Required Skills: ", "").split(',')
    
    missing_skills = [skill.strip() for skill in required_skills if skill.strip() not in user_skills]
    return missing_skills, required_skills

# Function to recommend adaptive learning pathways
def recommend_adaptive_learning_pathway(missing_skills, user_feedback):
    prompt = f"""
    Based on the following skills that the user needs to improve, and their feedback on previous courses, recommend a personalized learning pathway including a mix of micro-courses, webinars, and hands-on projects.

    Missing Skills: {', '.join(missing_skills)}
    User Feedback: {user_feedback}
    Recommended Learning Pathway: """

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
  
    return response.generations[0].text.replace("Recommended Learning Pathway: ", "").split('\n')

# Function to collect feedback on completed courses
def collect_course_feedback():
    st.subheader("📊 Course Feedback")
    feedback_form = st.form(key="course_feedback_form")
    
    with feedback_form:
        feedback_input = st.text_area("Provide your feedback on the recommended courses (e.g., Did it help you? Was it too advanced or too basic?)", key="feedback_input")
        submit_feedback = feedback_form.form_submit_button("Submit Feedback")
    
    if submit_feedback:
        if feedback_input == "":
            st.error("Feedback cannot be blank")
        else:
            st.session_state['course_feedback'] = feedback_input
            st.success("Thank you for your feedback!")
            st.rerun()

# Step 1: Get user's profile, skills, or resume
st.title("💼 Candidate Profile Evaluator")

# Allow user to upload resume
resume_upload = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])

# Function to read uploaded resume and extract text
def read_resume(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            return extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(uploaded_file)
    return ""

# If resume is uploaded, extract skills
if resume_upload:
    resume_text = read_resume(resume_upload)
    if resume_text:
        # Extract skills from resume using Cohere
        if 'skills_list' not in st.session_state:
            st.session_state['skills_list'] = extract_skills_from_resume(resume_text)
            st.session_state['profile_input'] = "Resume-based profile"
            st.rerun()  # Only rerun if the session state was modified

# If resume is not uploaded or skills are still empty, show manual profile input form
if not st.session_state.get('profile_input') and not st.session_state.get('skills_list'):
    form_profile = st.form(key="user_profile")
    with form_profile:
        profile_input = st.text_input("Briefly describe your profile (e.g., Software Engineer with 3 years of experience)", key="profile_input_input")
        skills_input = st.text_input("List your skills (comma-separated)", key="skills_input")
        
        submit_profile = form_profile.form_submit_button("Submit Profile and Skills")

    if submit_profile:
        if profile_input == "" or skills_input == "":
            st.error("Profile and skills fields cannot be blank")
        else:
            st.session_state['profile_input'] = profile_input
            st.session_state['skills_list'] = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
            st.rerun()

# Step 2: Ask user to rate the skills (if skills are provided)
if st.session_state.get('skills_list'):
    st.subheader("Rate your skills from 1 to 10")

    form_ratings = st.form(key="user_ratings")
    skills_ratings = {}
    
    for skill in st.session_state['skills_list']:
        skills_ratings[skill] = form_ratings.slider(f"{skill}", 1, 10, 5, key=f"{skill}_rating")
    
    submit_ratings = form_ratings.form_submit_button("Evaluate Profile")

    if submit_ratings:
        my_bar = st.progress(0.05)

        # Step 3: Find skill gaps
        missing_skills = find_skill_gaps(st.session_state['profile_input'], skills_ratings)
        st.subheader("🔍 Skill Gaps and Suggested Improvements")
        if missing_skills:
            st.write("The following skills need improvement or could be learned additionally:")
            st.write(", ".join(missing_skills))
        else:
            st.write("No skill gaps found. You're doing great!")

        # Step 4: Recommend courses
        st.subheader("📚 Recommended Courses")
        courses = recommend_courses(missing_skills)
        for i, course in enumerate(courses[:5]):
            st.write(f"{i+1}. {course}")

        # Step 5: Recommend jobs
        st.subheader("💼 Recommended Jobs")
        jobs = recommend_jobs(st.session_state['profile_input'])
        for i, job in enumerate(jobs[:5]):
            st.write(f"{i+1}. {job}")
        
        my_bar.progress(1.0)

# Step 6: Get user's desired job role for skill gap analysis
st.subheader("🎯 Desired Job Role")
job_role_input = st.text_input("Enter your desired job role (e.g., Data Scientist, Software Engineer)", key="job_role_input")

# If both skills and job role are provided, compare skills with job role requirements
if st.session_state.get('skills_list') and job_role_input:
    st.subheader(f"🔍 Skill Gap Analysis for '{job_role_input}'")
    
    # Compare user's skills with job role requirements
    missing_skills, required_skills = compare_skills_with_job_role(st.session_state['skills_list'], job_role_input)
    
    # Show missing skills and required skills
