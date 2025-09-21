import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from utils.pdf_processor import extract_text_from_pdf
from utils.resume_analyzer import analyze_resume_with_jd
from utils.gap_analyzer import perform_gap_analysis
from utils.roadmap_generator import generate_career_roadmap
from utils.mentor import get_ai_mentor_response
from utils.parser import parse_resume_with_ai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Prospello",
    page_icon="🚀",
    layout="wide"
)

# --- LOAD STYLES ---
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

load_css("styles.css")

# --- SESSION STATE INITIALIZATION ---
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = ""
if 'editable_resume_text' not in st.session_state:
    st.session_state.editable_resume_text = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
# FIX: Initialized as a DataFrame for stability
if "job_applications" not in st.session_state:
    st.session_state.job_applications = []


def clear_session_state():
    """Clears all data from the session state to start over."""
    for key in st.session_state.keys():
        del st.session_state[key]
    st.success("Session cleared! You can now upload a new resume.")

# --- SIDEBAR ---
with st.sidebar:
    try:
        # Simplified logo insertion: Read the file and encode it directly here
        with open("logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
            <div class="sidebar-header">
                <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo">
                <div class="sidebar-title">Prospello 🚀</div>
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        # If logo.png is not found, just display the title
        st.title("Prospello 🚀")

    st.markdown("From Resume to Role, We Guide Your Goal.")
    st.markdown("---") # Added horizontal line

    st.markdown("<div class='sidebar-menu'>", unsafe_allow_html=True)
    
    st.markdown("<h5>NAVIGATION</h5>", unsafe_allow_html=True) # Added Navigation heading
    
    # Using the simplified page names
    PAGES = ["🏠 Home", "📄 Preview", "📊 Analysis", "🔍 Compare", "🗺️ Roadmap", "💭 AI Mentor", "📈 Tracker", "ℹ️ About", "📧 Feedback"]
    
    page = st.radio(
        "Navigation", 
        PAGES,
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)


# --- MAIN PAGE ROUTING AND CONTENT ---
st.markdown("<div class='page-container'>", unsafe_allow_html=True)

if page == "🏠 Home":
    st.markdown("<h1 class='page-header'>WELCOME TO PROSPELLO</h1>", unsafe_allow_html=True)
    st.markdown("""
    Your all-in-one AI-powered assistant designed to help you navigate the complexities of the job market with confidence. 
    To begin, please upload your resume below. The AI will analyze it to provide personalized feedback and guidance across all modules.
    """)

    # If a resume is already uploaded, show a success message and the option to start over
    if st.session_state.resume_text:
        st.success("A resume has been successfully uploaded and analyzed.")
        st.info("You can now navigate to other sections using the sidebar.")
        
        if st.button("Upload Another Resume"):
            clear_session_state()
            st.rerun()
    
    # If no resume is uploaded, show the file uploader
    else:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            with st.spinner('Extracting text from your resume...'):
                resume_text = extract_text_from_pdf(uploaded_file)
                st.session_state.resume_text = resume_text
            st.success("Resume uploaded successfully!")
            # Automatically rerun to update the page view
            st.rerun()

elif page == "📄 Preview":
    st.markdown("<h1 class='page-header'>AI-POWERED RESUME DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("Our AI has read your resume and extracted the key details into a structured dashboard.")

    if 'resume_text' in st.session_state and st.session_state.resume_text is not None:
        
        with st.spinner("🤖 AI is reading and structuring your resume... This may take a moment."):
            extracted_details = parse_resume_with_ai(st.session_state.resume_text)
        
        if "error" in extracted_details:
            st.error(f"Could not parse resume: {extracted_details['error']}")
            st.info("This can happen if the API key is missing or invalid. Please check the key in 'utils/parser.py'.")
        else:
            # --- Display Profile ---
            profile = extracted_details.get('profile', {})
            st.markdown(f"""
            <div class="preview-card">
                <div class="preview-title">👤 Professional Profile</div>
                <p><strong>Name:</strong> {profile.get('name', 'N/A')}</p>
                <p><strong>Email:</strong> {profile.get('email', 'N/A')}</p>
                <p><strong>Phone:</strong> {profile.get('phone', 'N/A')}</p>
                <p><strong>LinkedIn:</strong> {profile.get('linkedin', 'N/A')}</p>
                <p><strong>GitHub:</strong> {profile.get('github', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

            # --- Display Summary ---
            st.markdown(f"""
            <div class="preview-card">
                <div class="preview-title">📝 Summary</div>
                <p>{extracted_details.get('summary', 'Not found.')}</p>
            </div>
            """, unsafe_allow_html=True)

            # --- Display Skills ---
            skills = extracted_details.get('skills', {})
            st.markdown('<div class="preview-card">', unsafe_allow_html=True)
            st.markdown('<div class="preview-title">🛠️ Skills</div>', unsafe_allow_html=True)
            if skills.get('programming'):
                st.markdown("<h6>Programming</h6>", unsafe_allow_html=True)
                st.markdown(f"<div class='skill-pills'>{''.join([f'<span class=skill-pill>{s}</span>' for s in skills['programming']])}</div>", unsafe_allow_html=True)
            if skills.get('tools_platforms'):
                st.markdown("<h6>Tools & Platforms</h6>", unsafe_allow_html=True)
                st.markdown(f"<div class='skill-pills'>{''.join([f'<span class=skill-pill>{s}</span>' for s in skills['tools_platforms']])}</div>", unsafe_allow_html=True)
            if skills.get('libraries_frameworks'):
                st.markdown("<h6>Libraries & Frameworks</h6>", unsafe_allow_html=True)
                st.markdown(f"<div class='skill-pills'>{''.join([f'<span class=skill-pill>{s}</span>' for s in skills['libraries_frameworks']])}</div>", unsafe_allow_html=True)
            if skills.get('soft_skills'):
                st.markdown("<h6>Soft Skills</h6>", unsafe_allow_html=True)
                st.markdown(f"<div class='skill-pills soft'>{''.join([f'<span class=skill-pill-soft>{s}</span>' for s in skills['soft_skills']])}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


            # --- Display Experience ---
            st.markdown('<div class="preview-card">', unsafe_allow_html=True)
            st.markdown('<div class="preview-title">💼 Experience</div>', unsafe_allow_html=True)
            for job in extracted_details.get('experience', []):
                st.markdown(f"<strong>{job.get('role', 'N/A')}</strong> at {job.get('company', 'N/A')}", unsafe_allow_html=True)
                st.caption(job.get('dates', 'N/A'))
                for resp in job.get('responsibilities', []):
                    st.markdown(f"- {resp}")
                if job != extracted_details.get('experience', [])[-1]:
                    st.markdown("---")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Display Projects ---
            st.markdown('<div class="preview-card">', unsafe_allow_html=True)
            st.markdown('<div class="preview-title">🚀 Projects</div>', unsafe_allow_html=True)
            for project in extracted_details.get('projects', []):
                st.markdown(f"<strong>{project.get('name', 'N/A')}</strong>", unsafe_allow_html=True)
                st.caption(f"Link: {project.get('link', 'N/A')}")
                st.write(project.get('description', ''))
                if project != extracted_details.get('projects', [])[-1]:
                    st.markdown("---")
            st.markdown('</div>', unsafe_allow_html=True)


    else:
        st.warning("Please upload your resume on the Home page first to see the preview.")

elif page == "📊 Analysis":
    st.markdown("<h1 class='page-header'>YOUR ADVANCED ANALYSIS DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("This dashboard combines high-level scores with a deep, detailed analysis of your resume.")

    if 'resume_text' not in st.session_state or st.session_state.resume_text is None:
        st.warning("Please upload your resume on the Home page first.")
    else:
        jd_text = st.text_area("Paste the Job Description here to generate your dashboard:", height=200, key="resume_jd")

        if st.button("Analyze Resume", type="primary"):
            if jd_text:
                try:
                    with st.spinner("Performing deep analysis with Prospello... This may take a moment."):
                        analysis = analyze_resume_with_jd(st.session_state.resume_text, jd_text)

                    if "error" in analysis:
                         st.error(f"🚨 An error occurred during analysis: {analysis['error']}")
                    else:
                        # --- RENDER THE 4-SCORE METRICS DASHBOARD ---
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(f"<div class='metric-card'><div class='metric-value'>{analysis.get('ats_match_score', 0)}%</div><div class='metric-label'>ATS Match Score</div></div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"<div class='metric-card'><div class='metric-value'>{analysis.get('experience_relevance_score', 0)}%</div><div class='metric-label'>Experience Relevance</div></div>", unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"<div class='metric-card'><div class='metric-value'>{analysis.get('keyword_score', 0)}%</div><div class='metric-label'>Keyword Score</div></div>", unsafe_allow_html=True)
                        with col4:
                            st.markdown(f"<div class='metric-card'><div class='metric-value'>{analysis.get('formatting_score', 0)}%</div><div class='metric-label'>Formatting Score</div></div>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("---")

                        # --- RENDER THE DEFINITIVE 10-POINT REPORT USING 9 EXPANDERS ---
                        
                        st.subheader("Detailed Analysis Report")

                        with st.expander("1. 👤 Profile Summary (Auto-Extracted)", expanded=True):
                            summary = analysis.get('profile_summary', {})
                            st.markdown(f"**Name:** `{summary.get('name', 'N/A')}`")
                            st.markdown(f"**Contact:** `{summary.get('contact', 'N/A')}`")
                            st.markdown(f"**Education:** `{summary.get('education', 'N/A')}`")
                            st.markdown(f"**Years of Experience:** `{summary.get('experience_years', 'N/A')}`")
                            st.markdown(f"**Key Skills Found:** `{' | '.join(summary.get('key_skills', ['None']))}`")

                        with st.expander("2. 🎯 Skills Match Analysis", expanded=True):
                            skills = analysis.get('skills_match', {})
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                st.markdown("<h6>✅ Matched</h6>", unsafe_allow_html=True)
                                for skill in skills.get('matched', []): st.markdown(f"<span class='skill-pill matched'>{skill}</span>", unsafe_allow_html=True)
                            with c2:
                                st.markdown("<h6>❌ Missing</h6>", unsafe_allow_html=True)
                                for skill in skills.get('missing', []): st.markdown(f"<span class='skill-pill missing'>{skill}</span>", unsafe_allow_html=True)
                            with c3:
                                st.markdown("<h6>💡 Recommended</h6>", unsafe_allow_html=True)
                                for skill in skills.get('recommended', []): st.markdown(f"<span class='skill-pill recommended'>{skill}</span>", unsafe_allow_html=True)
                            
                        with st.expander("3. 🔑 Keyword Optimization", expanded=True):
                            keywords = analysis.get('keyword_optimization', {})
                            st.markdown(f"**- Missing Keywords from JD:** `{' | '.join(keywords.get('missing_keywords', ['None']))}`")
                            st.markdown(f"**- Weak Keywords to Avoid:** `{' | '.join(keywords.get('weak_keywords', ['None']))}`")
                        
                        with st.expander("4. 💼 Experience Relevance", expanded=True):
                             exp_score = analysis.get('experience_relevance_score', 0)
                             st.markdown(f"Your experience appears to be **{exp_score}%** relevant to the job description based on contextual analysis.")
                             if exp_score < 60:
                                 st.warning("Consider tailoring your experience descriptions with keywords and quantifiable achievements to better match the role's requirements.")
                             else:
                                 st.success("Your experience is well-aligned with the job description.")

                        with st.expander("5. 🎓 Education & Certifications Check", expanded=True):
                            certs = analysis.get('education_certifications', {})
                            st.markdown(f"**- Required Certs Missing:** `{' | '.join(certs.get('missing', ['None']))}`")
                            st.markdown(f"**- Suggested Certifications:** `{' | '.join(certs.get('suggested', ['None']))}`")

                        with st.expander("6. 🤝 Soft Skills & Leadership Analysis", expanded=True):
                            soft = analysis.get('soft_skills_analysis', {})
                            st.markdown(f"**- Soft Skills Found:** `{' | '.join(soft.get('found', ['None']))}`")
                            st.markdown(f"**- Soft Skills Missing from JD:** `{' | '.join(soft.get('missing', ['None']))}`")

                        with st.expander("7. 📄 Formatting & ATS Readiness", expanded=True):
                            formatting = analysis.get('formatting_ats', {})
                            st.markdown(f"**- Structure Check:** `{formatting.get('structure', 'N/A')}`")
                            st.markdown(f"**- Formatting Issues:** `{formatting.get('issues', 'N/A')}`")
                            st.progress(analysis.get('formatting_score', 0), text=f"ATS Friendliness Score: {analysis.get('formatting_score', 0)}%")
                        
                        with st.expander("8. 🚀 Top Improvement Suggestions", expanded=True):
                            suggestions = analysis.get('improvement_suggestions', [])
                            if suggestions:
                                for suggestion in suggestions:
                                    st.markdown(f"- {suggestion}")
                            else:
                                st.info("No critical improvement suggestions found. Great job!")

                        with st.expander("9. 📥 Final Report (Download)", expanded=False):
                            report = analysis.get('final_report', {})
                            st.markdown(f"**- Overall Resume Score:** `{report.get('resume_score', 'N/A')}`")
                            st.markdown(f"**- JD Match Score:** `{report.get('jd_match_score', 'N/A')}`")
                            st.info("Downloadable PDF report feature is coming soon!")

                except Exception as e:
                    st.error(f"🚨 A critical error occurred while displaying the report.")
                    st.error(f"Error details: {e}")
            else:
                st.error("Please paste a job description to start the analysis.")

elif page == "🔍 Compare":
    st.markdown("<h1 class='page-header'>JD COMPARISON & GAP ANALYSIS</h1>", unsafe_allow_html=True)
    st.markdown("Instantly see how your skills stack up against a job description and get actionable advice.")

    if 'resume_text' not in st.session_state or st.session_state.resume_text is None:
        st.warning("Please upload your resume on the Home page first.")
    else:
        jd_text_comparison = st.text_area("Paste the Job Description here:", height=200, key="jd_compare")

        if st.button("Compare Resume to JD", type="primary"):
            if jd_text_comparison:
                with st.spinner("Performing AI-powered gap analysis..."):
                    analysis = perform_gap_analysis(st.session_state.resume_text, jd_text_comparison)

                if "error" in analysis:
                    st.error(f"🚨 Analysis Failed: {analysis['error']}")
                else:
                    st.markdown(f"<div class='fit-score-container'>Overall Fit Score: <span class='fit-score'>{analysis.get('fit_score', 0)}%</span></div>", unsafe_allow_html=True)
                    st.info(f"**Summary:** {analysis.get('analysis_summary', 'No summary available.')}")
                    st.markdown("---")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("<h5>✅ Matched Skills</h5>", unsafe_allow_html=True)
                        for skill in analysis.get('skill_analysis', {}).get('matched_skills', []):
                            st.markdown(f"<span class='skill-tag matched'>{skill}</span>", unsafe_allow_html=True)
                    with col2:
                        st.markdown("<h5>❌ Missing Skills</h5>", unsafe_allow_html=True)
                        for skill in analysis.get('skill_analysis', {}).get('missing_skills', []):
                            st.markdown(f"<span class='skill-tag missing'>{skill}</span>", unsafe_allow_html=True)
                    with col3:
                        st.markdown("<h5>⭐ Your Unique Skills</h5>", unsafe_allow_html=True)
                        for skill in analysis.get('skill_analysis', {}).get('unique_skills', []):
                            st.markdown(f"<span class='skill-tag unique'>{skill}</span>", unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown("<h4>Actionable Next Steps</h4>", unsafe_allow_html=True)
                    next_steps = analysis.get('next_steps', [])
                    for step in next_steps:
                        with st.container():
                            st.markdown(f"<h5>{step.get('title')}</h5>", unsafe_allow_html=True)
                            st.write(step.get('suggestion'))
                            st.success(f"**Recommended Action:** {step.get('action')}")
            else:
                st.error("Please paste a job description to perform the analysis.")

elif page == "🗺️ Roadmap":
    st.markdown("<h1 class='page-header'>PERSONALIZED CAREER ROADMAP</h1>", unsafe_allow_html=True)
    st.markdown("Get a step-by-step plan to bridge the gap and achieve your career goals, tailored to your resume.")

    if 'resume_text' not in st.session_state or st.session_state.resume_text is None:
        st.warning("Please upload your resume on the Home page first to generate a roadmap.")
    else:
        # --- Roadmap Type Selection ---
        roadmap_type = st.radio(
            "Select Roadmap Type:",
            ("By Job Role", "By Job Description"),
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown("---")

        if roadmap_type == "By Job Role":
            job_role = st.text_input("Enter your target job role (e.g., 'Data Scientist', 'Frontend Developer'):")
            if st.button("Generate Roadmap by Role", type="primary"):
                if job_role:
                    with st.spinner(f"Generating a 30-day roadmap to become a {job_role}..."):
                        roadmap_result = generate_career_roadmap(st.session_state.resume_text, job_role, "Job Role")
                        
                        st.subheader(f"Your Roadmap to a {job_role} Role")
                        st.markdown(roadmap_result)
                else:
                    st.error("Please enter a job role.")

        elif roadmap_type == "By Job Description":
            jd_text = st.text_area("Paste the full Job Description here:", height=250)
            if st.button("Generate Roadmap by JD", type="primary"):
                if jd_text:
                    with st.spinner("Analyzing the job description and generating your personalized roadmap..."):
                        roadmap_result = generate_career_roadmap(st.session_state.resume_text, jd_text, "Job Description")

                        st.subheader("Your Roadmap for this Specific Role")
                        st.markdown(roadmap_result)
                else:
                    st.error("Please paste a job description.")

elif page == "💭 AI Mentor":
    st.markdown("<h1 class='page-header'>AI CAREER MENTOR</h1>", unsafe_allow_html=True)
    st.markdown("Ask me anything about career advice, interview tips, or skill development! I can see your resume to give you personalized feedback.")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you with your career today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to ask?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                resume_context = st.session_state.get('resume_text', "The user has not uploaded a resume yet.")
                full_response = get_ai_mentor_response(prompt, st.session_state.messages, resume_context)
                message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif page == "📈 Tracker":
    st.markdown("<h1 class='page-header'>JOB APPLICATION TRACKER</h1>", unsafe_allow_html=True)
    st.markdown("Visually track your job applications from start to finish using this interactive Kanban board.")

    with st.expander("➕ Add a New Job Application", expanded=False):
        with st.form("new_app_form", clear_on_submit=True):
            # ... Form content remains the same ...
            new_company = st.text_input("Company Name*")
            new_title = st.text_input("Job Title*")
            new_status = st.selectbox("Current Status", ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"])
            
            submitted = st.form_submit_button("Add Application")
            if submitted and new_company and new_title:
                st.session_state.job_applications.append({
                    "id": len(st.session_state.job_applications) + 1,
                    "company": new_company,
                    "title": new_title,
                    "status": new_status,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                st.rerun()

    st.markdown("---")

    statuses = ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"]
    cols = st.columns(len(statuses))

    for i, status in enumerate(statuses):
        with cols[i]:
            st.markdown(f"<h3 class='kanban-header'>{status}</h3>", unsafe_allow_html=True)
            apps_in_status = [app for app in st.session_state.job_applications if app['status'] == status]
            
            if not apps_in_status:
                st.markdown("<div class='kanban-card-empty'>No applications</div>", unsafe_allow_html=True)

            for app in apps_in_status:
                with st.container():
                    st.markdown(f"""
                        <div class='kanban-card'>
                            <div class='kanban-card-title'>{app['title']}</div>
                            <div class='kanban-card-company'>{app['company']}</div>
                            <div class='kanban-card-date'>Added: {app['date']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    new_status = st.selectbox("Move to:", options=statuses, index=statuses.index(app['status']), key=f"status_{app['id']}", label_visibility="collapsed")
                    if new_status != app['status']:
                        app['status'] = new_status
                        st.rerun()
                    
                    if st.button("Delete", key=f"delete_{app['id']}", type="secondary"):
                        st.session_state.job_applications.remove(app)
                        st.rerun()

elif page == "ℹ️ About":
    st.markdown("<h1 class='page-header'>ABOUT PROSPELLO</h1>", unsafe_allow_html=True)
    st.info("**Our Mission:** To empower job seekers with intelligent tools that provide clear, personalized, and actionable guidance for their career journey.")
    st.markdown("""
    **Prospello** is more than just a tool—it's your personal AI career companion. In today's competitive job market, a great resume and a clear strategy are essential. We built Prospello to bridge the gap between your skills and the jobs you want, transforming a stressful process into a confident and organized journey.
    """)
    st.markdown("---")

    st.markdown("### Key Features at a Glance")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📄 Smart Resume Parsing")
        st.markdown("Our AI reads and understands your resume, extracting key details to power all our analysis modules.")
        
        st.markdown("#### 🗺️ AI-Powered Roadmaps")
        st.markdown("Get custom, 30-day action plans to bridge skill gaps for a specific job or a new career path.")

    with col2:
        st.markdown("#### 📊 Advanced Analysis")
        st.markdown("Receive a detailed, 10-point analysis of your resume against any job description, with actionable feedback.")

        st.markdown("#### 📈 Visual Job Tracker")
        st.markdown("Organize your job search with our interactive Kanban board, tracking applications from 'Wishlist' to 'Offer'.")

    with col3:
        st.markdown("#### 🔍 Intelligent Gap Analysis")
        st.markdown("Instantly see how your skills and experience stack up against a job description's requirements.")

        st.markdown("#### 🤖 24/7 AI Mentor")
        st.markdown("Chat with our AI career coach for personalized advice, interview prep, and answers to your career questions.")

    st.markdown("---")
    st.markdown("### Powered by Advanced AI")
    st.markdown("CareerCoPilot's intelligent features, from resume parsing to the AI mentor, are powered by Google's state-of-the-art Gemini models. This ensures you receive nuanced, contextual, and highly relevant guidance.")

    st.markdown("---")
    st.markdown("### Meet the Developer")
    st.markdown("This application was designed and built with a passion for helping job seekers succeed. Connect with the developer, **Habib**, on [LinkedIn](https://www.linkedin.com/in/halcyon-habib).")

elif page == "📧 Feedback":
    st.markdown("<h1 class='page-header'>SUBMIT YOUR FEEDBACK</h1>", unsafe_allow_html=True)
    st.markdown("We are constantly working to improve Prospello. Your feedback is invaluable to us!")

    with st.form("feedback_form", clear_on_submit=True):
        st.subheader("How would you rate your experience with Prospello?")
        rating = st.slider("Rate from 1 (Poor) to 5 (Excellent)", 1, 5, 3)
        
        st.subheader("Share your detailed feedback:")
        feedback_text = st.text_area("What did you like? What could be better? Please be as specific as possible.", height=200)
        
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            st.success("Thank you for your feedback! We appreciate you helping us make Prospello even better.")
            st.balloons()

st.markdown("</div>", unsafe_allow_html=True)

