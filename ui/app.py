import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="AI Resume Booster - LaTeX Edition",
    page_icon="📝",
    layout="wide"
)

# CUSTOM CSS
st.markdown( """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2563eb;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #cbd5e1;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #dcfce7;
        border-left: 4px solid #16a34a;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True )

# INITIALIZE SESSION STATE
if "resume_data" not in st.session_state :
    st.session_state.resume_data = {
        "personal_info" : {},
        "education" : [],
        "experience" : [],
        "projects" : [],
        "skills" : [],
        "certifications" : [],
        "links" : {}
    }

if "uploaded_files" not in st.session_state :
    st.session_state.uploaded_files = {}

# HEADER
st.markdown( '<div class="main-header">AI Resume Booster - LaTeX Edition</div>', unsafe_allow_html=True )
st.markdown( '<div class="sub-header">Create Professional LaTeX Resumes with Certificates & Portfolio Links</div>',
             unsafe_allow_html=True )

# SIDEBAR - TEMPLATE SELECTION
st.sidebar.title( "LaTeX Template Selection" )

latex_templates = {
    "modern_deedy" : "Modern Deedy (Single Column)",
    "awesome_cv" : "Awesome CV (Professional)",
    "classic_altacv" : "Classic AltaCV (Two Column)",
    "academic" : "Academic CV (Traditional)",
    "tech_resume" : "Tech Resume (Developer Focused)",
    "minimalist" : "Minimalist (Clean & Simple)"
}

selected_template = st.sidebar.selectbox(
    "Choose LaTeX Template:",
    list( latex_templates.keys() ),
    format_func=lambda x : latex_templates[x]
)

st.sidebar.markdown( "---" )
st.sidebar.markdown( "### Industry Focus" )

industry = st.sidebar.selectbox(
    "Select Industry:",
    ["Technology", "Finance", "Marketing", "Healthcare", "Education", "Research/Academic", "General"]
)

# MAIN TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs( [
    "Personal Info",
    "Education & Certs",
    "Experience",
    "Projects & Links",
    "Generate Resume",
    "Upload Resume"
] )

# TAB 1: PERSONAL INFORMATION
with tab1 :
    st.markdown( "### Personal Information" )

    col1, col2 = st.columns( 2 )

    with col1 :
        name = st.text_input( "Full Name*", value=st.session_state.resume_data["personal_info"].get( "name", "" ) )
        email = st.text_input( "Email*", value=st.session_state.resume_data["personal_info"].get( "email", "" ) )
        phone = st.text_input( "Phone", value=st.session_state.resume_data["personal_info"].get( "phone", "" ) )

    with col2 :
        location = st.text_input( "Location (City, State)",
                                  value=st.session_state.resume_data["personal_info"].get( "location", "" ) )
        linkedin = st.text_input( "LinkedIn URL",
                                  value=st.session_state.resume_data["personal_info"].get( "linkedin", "" ) )
        website = st.text_input( "Portfolio/Website",
                                 value=st.session_state.resume_data["personal_info"].get( "website", "" ) )

    github = st.text_input( "GitHub Profile", value=st.session_state.resume_data["personal_info"].get( "github", "" ) )

    summary = st.text_area(
        "Professional Summary",
        value=st.session_state.resume_data["personal_info"].get( "summary", "" ),
        height=100,
        placeholder="Brief professional summary highlighting your key strengths and career objectives..."
    )

    if st.button( "Save Personal Info", type="primary" ) :
        st.session_state.resume_data["personal_info"] = {
            "name" : name,
            "email" : email,
            "phone" : phone,
            "location" : location,
            "linkedin" : linkedin,
            "website" : website,
            "github" : github,
            "summary" : summary
        }
        st.success( "Personal information saved!" )

# TAB 2: EDUCATION & CERTIFICATIONS
with tab2 :
    st.markdown( "### Education" )

    # Add Education
    with st.expander( "Add Education", expanded=True ) :
        edu_col1, edu_col2 = st.columns( 2 )

        with edu_col1 :
            edu_degree = st.text_input( "Degree", key="edu_degree" )
            edu_institution = st.text_input( "Institution", key="edu_institution" )
            edu_gpa = st.text_input( "GPA (optional)", key="edu_gpa" )

        with edu_col2 :
            edu_field = st.text_input( "Field of Study", key="edu_field" )
            edu_graduation = st.text_input( "Graduation Date", key="edu_graduation" )
            edu_location = st.text_input( "Location", key="edu_location" )

        edu_achievements = st.text_area(
            "Relevant Coursework / Achievements",
            key="edu_achievements",
            placeholder="Dean's List, Relevant coursework, Academic honors..."
        )

        if st.button( "Add Education Entry" ) :
            if edu_degree and edu_institution :
                st.session_state.resume_data["education"].append( {
                    "degree" : edu_degree,
                    "field" : edu_field,
                    "institution" : edu_institution,
                    "location" : edu_location,
                    "graduation" : edu_graduation,
                    "gpa" : edu_gpa,
                    "achievements" : edu_achievements
                } )
                st.success( "Education entry added!" )
                st.rerun()

    # Display Education Entries
    if st.session_state.resume_data["education"] :
        st.markdown( "#### Current Education Entries" )
        for i, edu in enumerate( st.session_state.resume_data["education"] ) :
            with st.container() :
                col1, col2 = st.columns( [5, 1] )
                with col1 :
                    st.markdown( f"**{edu['degree']}** in {edu['field']} - {edu['institution']}" )
                    st.caption( f"{edu['graduation']} | GPA: {edu['gpa']}" )
                with col2 :
                    if st.button( "Delete", key=f"del_edu_{i}" ) :
                        st.session_state.resume_data["education"].pop( i )
                        st.rerun()
                st.markdown( "---" )

    # Certifications Section
    st.markdown( "### Certifications" )

    with st.expander( "Add Certification", expanded=True ) :
        cert_col1, cert_col2 = st.columns( 2 )

        with cert_col1 :
            cert_name = st.text_input( "Certification Name", key="cert_name" )
            cert_issuer = st.text_input( "Issuing Organization", key="cert_issuer" )

        with cert_col2 :
            cert_date = st.text_input( "Issue Date", key="cert_date" )
            cert_id = st.text_input( "Credential ID (optional)", key="cert_id" )

        cert_url = st.text_input( "Verification URL", key="cert_url", placeholder="https://..." )

        # Certificate Upload
        st.markdown( "#### Upload Certificate (Optional)" )
        cert_file = st.file_uploader(
            "Upload certificate image/PDF",
            type=["pdf", "jpg", "jpeg", "png"],
            key="cert_upload"
        )

        if st.button( "Add Certification" ) :
            if cert_name and cert_issuer :
                cert_entry = {
                    "name" : cert_name,
                    "issuer" : cert_issuer,
                    "date" : cert_date,
                    "credential_id" : cert_id,
                    "url" : cert_url
                }

                # Handle file upload
                if cert_file :
                    file_bytes = cert_file.read()
                    file_b64 = base64.b64encode( file_bytes ).decode()
                    cert_entry["file"] = {
                        "name" : cert_file.name,
                        "type" : cert_file.type,
                        "data" : file_b64
                    }
                    st.session_state.uploaded_files[f"cert_{cert_name}"] = cert_file.name

                st.session_state.resume_data["certifications"].append( cert_entry )
                st.success( "Certification added!" )
                st.rerun()

    # Display Certifications
    if st.session_state.resume_data["certifications"] :
        st.markdown( "#### Current Certifications" )
        for i, cert in enumerate( st.session_state.resume_data["certifications"] ) :
            with st.container() :
                col1, col2 = st.columns( [5, 1] )
                with col1 :
                    st.markdown( f"**{cert['name']}** - {cert['issuer']}" )
                    st.caption( f"Issued: {cert['date']} | ID: {cert['credential_id']}" )
                    if cert.get( 'url' ) :
                        st.caption( f"[Verify]({cert['url']})" )
                    if cert.get( 'file' ) :
                        st.caption( f"File: {cert['file']['name']}" )
                with col2 :
                    if st.button( "Delete", key=f"del_cert_{i}" ) :
                        st.session_state.resume_data["certifications"].pop( i )
                        st.rerun()
                st.markdown( "---" )

# TAB 3: WORK EXPERIENCE
with tab3 :
    st.markdown( "### Work Experience" )

    with st.expander( "Add Work Experience", expanded=True ) :
        exp_col1, exp_col2 = st.columns( 2 )

        with exp_col1 :
            exp_title = st.text_input( "Job Title", key="exp_title" )
            exp_company = st.text_input( "Company Name", key="exp_company" )
            exp_start = st.text_input( "Start Date", key="exp_start" )

        with exp_col2 :
            exp_location = st.text_input( "Location", key="exp_location" )
            exp_type = st.selectbox( "Employment Type",
                                     ["Full-time", "Part-time", "Internship", "Contract", "Freelance"], key="exp_type" )
            exp_end = st.text_input( "End Date (or 'Present')", key="exp_end" )

        exp_description = st.text_area(
            "Key Achievements & Responsibilities (one per line)",
            key="exp_description",
            height=150,
            placeholder="* Led team of 5 engineers to deliver project 2 weeks ahead of schedule\n* Increased efficiency by 40% through process automation\n* Reduced costs by $150K annually"
        )

        if st.button( "Add Experience Entry" ) :
            if exp_title and exp_company :
                st.session_state.resume_data["experience"].append( {
                    "title" : exp_title,
                    "company" : exp_company,
                    "location" : exp_location,
                    "type" : exp_type,
                    "start_date" : exp_start,
                    "end_date" : exp_end,
                    "description" : exp_description
                } )
                st.success( "Experience entry added!" )
                st.rerun()

    # Display Experience Entries
    if st.session_state.resume_data["experience"] :
        st.markdown( "#### Current Experience Entries" )
        for i, exp in enumerate( st.session_state.resume_data["experience"] ) :
            with st.container() :
                col1, col2 = st.columns( [5, 1] )
                with col1 :
                    st.markdown( f"**{exp['title']}** at {exp['company']}" )
                    st.caption( f"{exp['start_date']} - {exp['end_date']} | {exp['type']}" )
                with col2 :
                    if st.button( "Delete", key=f"del_exp_{i}" ) :
                        st.session_state.resume_data["experience"].pop( i )
                        st.rerun()
                st.markdown( "---" )

# TAB 4: PROJECTS & LINKS
with tab4 :
    st.markdown( "### Projects" )

    with st.expander( "Add Project", expanded=True ) :
        proj_col1, proj_col2 = st.columns( 2 )

        with proj_col1 :
            proj_name = st.text_input( "Project Name", key="proj_name" )
            proj_github = st.text_input( "GitHub Repository URL", key="proj_github" )

        with proj_col2 :
            proj_tech = st.text_input( "Technologies Used", key="proj_tech", placeholder="Python, React, AWS..." )
            proj_demo = st.text_input( "Live Demo URL (optional)", key="proj_demo" )

        proj_description = st.text_area(
            "Project Description & Achievements",
            key="proj_description",
            height=100,
            placeholder="Brief description of the project, your role, and key achievements..."
        )

        if st.button( "Add Project" ) :
            if proj_name :
                st.session_state.resume_data["projects"].append( {
                    "name" : proj_name,
                    "github" : proj_github,
                    "demo" : proj_demo,
                    "technologies" : proj_tech,
                    "description" : proj_description
                } )
                st.success( "Project added!" )
                st.rerun()

    # Display Projects
    if st.session_state.resume_data["projects"] :
        st.markdown( "#### Current Projects" )
        for i, proj in enumerate( st.session_state.resume_data["projects"] ) :
            with st.container() :
                col1, col2 = st.columns( [5, 1] )
                with col1 :
                    st.markdown( f"**{proj['name']}**" )
                    st.caption( f"Tech: {proj['technologies']}" )
                    if proj.get( 'github' ) :
                        st.caption( f"[GitHub]({proj['github']})" )
                    if proj.get( 'demo' ) :
                        st.caption( f"[Demo]({proj['demo']})" )
                with col2 :
                    if st.button( "Delete", key=f"del_proj_{i}" ) :
                        st.session_state.resume_data["projects"].pop( i )
                        st.rerun()
                st.markdown( "---" )

    # Skills Section
    st.markdown( "### Technical Skills" )

    skills_input = st.text_area(
        "Add skills (comma-separated)",
        key="skills_input",
        height=100,
        placeholder="Python, JavaScript, React, AWS, Docker, Machine Learning, Git..."
    )

    if st.button( "Save Skills" ) :
        if skills_input :
            st.session_state.resume_data["skills"] = [s.strip() for s in skills_input.split( ',' )]
            st.success( "Skills saved!" )

    if st.session_state.resume_data["skills"] :
        st.markdown( "**Current Skills:**" )
        st.write( ", ".join( st.session_state.resume_data["skills"] ) )

# TAB 5: GENERATE RESUME
with tab5 :
    st.markdown( "### Generate LaTeX Resume" )

    col1, col2 = st.columns( [2, 1] )

    with col1 :
        st.info( "Selected Template: **" + latex_templates[selected_template] + "**" )

    with col2 :
        if st.button( "Generate LaTeX & PDF", type="primary", use_container_width=True ) :
            with st.spinner( "Generating resume..." ) :
                try :
                    # Generate LaTeX
                    response = requests.post(
                        "http://127.0.0.1:8000/generate-latex",
                        json={
                            "resume_data" : st.session_state.resume_data,
                            "template" : selected_template,
                            "industry" : industry
                        },
                        timeout=30
                    ).json()

                    latex_code = response.get( "latex_code", "" )
                    st.session_state.latex_code = latex_code

                    # Try to compile PDF directly
                    try :
                        pdf_response = requests.post(
                            "http://127.0.0.1:8000/compile-pdf",
                            json={"latex_code" : latex_code},
                            timeout=60
                        )

                        if pdf_response.status_code == 200 :
                            st.success( "Resume generated successfully!" )

                            # Show download buttons
                            col_a, col_b = st.columns( 2 )

                            with col_a :
                                st.download_button(
                                    "Download PDF",
                                    pdf_response.content,
                                    file_name="resume.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )

                            with col_b :
                                st.download_button(
                                    "Download LaTeX (.tex)",
                                    latex_code,
                                    file_name="resume.tex",
                                    mime="text/plain",
                                    use_container_width=True
                                )
                        else :
                            st.warning( "PDF compilation not available. Generating using online compiler..." )

                            # Use Overleaf API-like approach or redirect
                            st.download_button(
                                "Download LaTeX (.tex)",
                                latex_code,
                                file_name="resume.tex",
                                mime="text/plain",
                                use_container_width=True
                            )

                            # Create Overleaf project link
                            import urllib.parse

                            encoded_latex = urllib.parse.quote( latex_code )
                            overleaf_url = f"https://www.overleaf.com/docs?snip_uri={encoded_latex}"

                            st.markdown( "Or compile online:" )
                            st.link_button( "Open in Overleaf", "https://www.overleaf.com/project",
                                            use_container_width=True )

                    except Exception as pdf_error :
                        st.warning( "PDF compilation not available. Generating using online compiler..." )

                        st.download_button(
                            "Download LaTeX (.tex)",
                            latex_code,
                            file_name="resume.tex",
                            mime="text/plain",
                            use_container_width=True
                        )

                        st.markdown( "Or compile online:" )
                        st.link_button( "Open in Overleaf", "https://www.overleaf.com/project",
                                        use_container_width=True )

                except Exception as e :
                    st.error( f"Error: {str( e )}" )

    # Display LaTeX Code Preview
    if "latex_code" in st.session_state and st.session_state.latex_code :
        st.markdown( "---" )
        st.markdown( "### LaTeX Code Preview" )
        with st.expander( "View LaTeX Code", expanded=False ) :
            st.code( st.session_state.latex_code, language="latex" )

# TAB 6: UPLOAD EXISTING RESUME
with tab6 :
    st.markdown( "### Upload Existing Resume" )

    st.markdown( """
    Upload your existing resume (PDF, DOCX, or TXT) and we'll extract the information 
    and convert it to LaTeX format.
    """ )

    uploaded_resume = st.file_uploader(
        "Choose your resume file",
        type=["pdf", "docx", "txt"],
        help="Upload PDF, DOCX, or TXT format"
    )

    if uploaded_resume :
        st.success( f"File uploaded: {uploaded_resume.name}" )

        if st.button( "Extract & Convert to LaTeX", type="primary" ) :
            with st.spinner( "Extracting information from resume..." ) :
                try :
                    files = {"file" : (uploaded_resume.name, uploaded_resume, uploaded_resume.type)}

                    response = requests.post(
                        "http://127.0.0.1:8000/extract-resume",
                        files=files,
                        timeout=60
                    ).json()

                    # Update session state with extracted data
                    if response.get( "success" ) :
                        st.session_state.resume_data = response.get( "resume_data", {} )
                        st.success( "Resume information extracted! Check other tabs to review and edit." )

                        # Show preview
                        st.markdown( "#### Extracted Information Preview" )
                        st.json( st.session_state.resume_data )
                    else :
                        st.error( "Failed to extract resume information" )

                except Exception as e :
                    st.error( f"Error: {str( e )}" )

# SIDEBAR - STATUS & TIPS
st.sidebar.markdown( "---" )
st.sidebar.markdown( "### System Status" )

try :
    health = requests.get( "http://127.0.0.1:8000/", timeout=2 ).json()
    st.sidebar.success( "Backend Online" )
except :
    st.sidebar.error( "Backend Offline" )
    st.sidebar.warning( "Start: uvicorn main:app --reload" )

st.sidebar.markdown( "---" )
st.sidebar.markdown( "### Quick Tips" )

st.sidebar.markdown( """
**LaTeX Resume Tips:**
- Keep it to 1-2 pages
- Use consistent formatting
- Quantify achievements
- Include relevant links
- Proofread carefully

**Project Links:**
- Add GitHub repos
- Include live demos
- Show diverse projects
- Highlight tech stack
""" )
