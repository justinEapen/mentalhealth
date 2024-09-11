import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Define template choices
TEMPLATES = {
    "Simple": "simple",
    "Modern": "modern",
    "Professional": "professional",
}

# Define template previews (use your own image files or URLs)
TEMPLATE_PREVIEWS = {
    "simple": "https://via.placeholder.com/300x200?text=Simple+Template",
    "modern": "https://via.placeholder.com/300x200?text=Modern+Template",
    "professional": "https://via.placeholder.com/300x200?text=Professional+Template",
}

def generate_pdf(template, name, email, phone, education, work_experience, skills, additional_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    
    if template == "simple":
        pdf.cell(200, 10, txt = f"Name: {name}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Email: {email}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Phone: {phone}", ln = True, align = 'L')
        
        pdf.ln(10)
        pdf.cell(200, 10, txt = "Education:", ln = True, align = 'L')
        pdf.multi_cell(0, 10, education)
        
        pdf.ln(10)
        pdf.cell(200, 10, txt = "Work Experience:", ln = True, align = 'L')
        pdf.multi_cell(0, 10, work_experience)
        
        pdf.ln(10)
        pdf.cell(200, 10, txt = "Skills:", ln = True, align = 'L')
        pdf.multi_cell(0, 10, skills)
        
        pdf.ln(10)
        pdf.cell(200, 10, txt = "Additional Information:", ln = True, align = 'L')
        pdf.multi_cell(0, 10, additional_info)

    elif template == "modern":
        pdf.set_font("Arial", size = 14, style = 'B')
        pdf.cell(200, 10, txt = name, ln = True, align = 'C')
        pdf.set_font("Arial", size = 12)
        pdf.cell(200, 10, txt = f"Email: {email} | Phone: {phone}", ln = True, align = 'C')
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Education", ln = True, align = 'L')
        pdf.set_font("Arial", size = 12)
        pdf.multi_cell(0, 10, education)
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Work Experience", ln = True, align = 'L')
        pdf.set_font("Arial", size = 12)
        pdf.multi_cell(0, 10, work_experience)
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Skills", ln = True, align = 'L')
        pdf.set_font("Arial", size = 12)
        pdf.multi_cell(0, 10, skills)
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Additional Information", ln = True, align = 'L')
        pdf.set_font("Arial", size = 12)
        pdf.multi_cell(0, 10, additional_info)
        
    elif template == "professional":
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = f"{name}", ln = True, align = 'C')
        pdf.set_font("Arial", size = 10)
        pdf.cell(200, 10, txt = f"Email: {email} | Phone: {phone}", ln = True, align = 'C')
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Education", ln = True, align = 'L')
        pdf.set_font("Arial", size = 10)
        pdf.multi_cell(0, 10, education)
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Work Experience", ln = True, align = 'L')
        pdf.set_font("Arial", size = 10)
        pdf.multi_cell(0, 10, work_experience)
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Skills", ln = True, align = 'L')
        pdf.set_font("Arial", size = 10)
        pdf.multi_cell(0, 10, skills)
        
        pdf.ln(10)
        pdf.set_font("Arial", size = 12, style = 'B')
        pdf.cell(200, 10, txt = "Additional Information", ln = True, align = 'L')
        pdf.set_font("Arial", size = 10)
        pdf.multi_cell(0, 10, additional_info)
    
    pdf_output = "resume.pdf"
    pdf.output(pdf_output)
    return pdf_output

def main():
    st.title("ResumeWizard")

    st.header("Choose Your Resume Template")

    # Display template previews and selection in the main section
    col1, col2, col3 = st.columns(3)
    
    # Template buttons
    with col1:
        if st.button("Simple Template"):
            st.session_state.selected_template = "simple"
    
    with col2:
        if st.button("Modern Template"):
            st.session_state.selected_template = "modern"
    
    with col3:
        if st.button("Professional Template"):
            st.session_state.selected_template = "professional"
    
    # Display selected template preview
    if "selected_template" in st.session_state:
        selected_template = st.session_state.selected_template
        if selected_template in TEMPLATE_PREVIEWS:
            st.image(TEMPLATE_PREVIEWS[selected_template], caption=f"{selected_template.capitalize()} Template", use_column_width=True)
        else:
            st.error("Template preview not found.")
    else:
        st.info("Please select a template to see the preview.")

    st.header("Enter Your Details")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    
    education = st.text_area("Education Details")
    work_experience = st.text_area("Work Experience Details")
    skills = st.text_area("Skills (Comma-separated)")
    additional_info = st.text_area("Additional Information")

    if st.button("Generate Resume"):
        if "selected_template" not in st.session_state:
            st.error("Please select a template before generating the resume.")
        elif not (name and email and phone and education and work_experience and skills):
            st.error("Please fill out all required fields.")
        else:
            pdf_file = generate_pdf(st.session_state.selected_template, name, email, phone, education, work_experience, skills, additional_info)
            st.success("Resume generated successfully!")
            with open(pdf_file, "rb") as file:
                st.download_button(label="Download Resume", data=file, file_name=pdf_file)

if __name__ == "__main__":
    main()
