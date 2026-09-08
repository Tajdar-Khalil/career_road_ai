import streamlit as st
import os
import json
from groq import Groq

# ---------------------------------------------------------
# Page Configuration & UI/UX Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Career Road - AI Career Guidance & Roadmap",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Modern CSS Styling
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 2.2rem 2rem;
        margin-bottom: 2rem;
        color: #f8fafc;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        max-width: 850px;
        line-height: 1.6;
    }

    /* Input Card Container */
    .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
        border-radius: 10px !important;
    }
    
    /* Highlight Cards */
    .metric-badge {
        display: inline-block;
        padding: 6px 14px;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid rgba(56, 189, 248, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Groq API Configuration
# ---------------------------------------------------------
# Set your free Groq API key here or via Streamlit Cloud Secrets (st.secrets["GROQ_API_KEY"])
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        GROQ_API_KEY = ""

# If not found in environment or secrets, fallback to your hardcoded key placeholder
if not GROQ_API_KEY:
    # REPLACE WITH YOUR ACTUAL GROQ API KEY IF HARDCODING IN CODE
    GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

# ---------------------------------------------------------
# Sidebar - About & User Guidance
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Career Road")
    st.markdown("Your personalized navigation engine for academic transitions, career roadmaps, and skills acceleration.")
    st.markdown("---")
    
    st.markdown("#### 🎯 Supported Academic Stages:")
    st.markdown("""
    - **Matric / O-Levels / 10th** (Choosing intermediate tracks: Pre-Engineering, Pre-Medical, ICS, I.Com, Arts)
    - **Intermediate / FSc / FA / A-Levels** (University degrees & entry strategies)
    - **BS / Undergraduate** (Career specializations, industry certifications & graduate roadmap)
    - **Self-Learner / Career Switcher**
    """)
    st.markdown("---")
    st.caption("Powered by **Groq Llama-3.3-70b-versatile** (Ultra-fast & free tier).")

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🧭 Career Road: Smart AI Career Counseling & Roadmap</div>
    <div class="hero-subtitle">
        Whether you just completed Matric/O-Levels, Intermediate/FSc, or your BS degree, get tailored career exploration, degree pathway advice, milestone-based roadmaps, and essential technical stacks.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Form Section - Clean Multi-column Layout
# ---------------------------------------------------------
with st.form("career_guidance_form"):
    st.markdown("### 📋 1. Your Academic & Experience Profile")
    col1, col2 = st.columns([1, 1])

    with col1:
        education_stage = st.selectbox(
            "Current Academic Stage / Milestone *",
            options=[
                "Completed Matric / 10th / O-Levels (Planning Intermediate / High School)",
                "Completed Intermediate / FSc / ICS / A-Levels (Planning University / BS)",
                "Currently Pursuing BS / Bachelor's Degree",
                "Graduated BS / Master's (Looking for Industry Entry / Specialization)",
                "Non-traditional / Self-Learner / Career Switcher"
            ],
            index=1
        )

        current_field = st.text_input(
            "Current Stream / Major / Subjects *",
            placeholder="e.g., Computer Science, Pre-Engineering, ICS, Commerce, Bio-Sciences, etc."
        )

    with col2:
        skill_level = st.select_slider(
            "Current Practical Skill Level *",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Beginner",
            help="Beginner: Just starting or foundational concepts. Intermediate: Can build small projects. Advanced: Working on complex systems or ready for senior roles."
        )

        target_course = st.text_input(
            "Specific Course or Degree You Are Thinking About (Optional)",
            placeholder="e.g., BS Data Science, Cloud Computing, ACCA, AI Engineering, Full Stack Web Dev, or leave blank"
        )

    st.markdown("### 💡 2. Interests & Career Direction")
    col3, col4 = st.columns([1, 1])

    with col3:
        user_interests = st.text_area(
            "What topics, hobbies, or domains excite you? (Leave blank if you have no clear interest)",
            placeholder="e.g., I enjoy problem-solving and coding, or I prefer creative design, or I want high-paying remote roles, or 'I have no specific interest yet, please suggest based on market demand.'",
            height=110
        )

    with col4:
        preference_mode = st.radio(
            "Career Exploration Mode",
            [
                "I know my target direction (Give me a deep roadmap & counseling)",
                "I am unsure / have no fixed interest (Suggest top 3 high-growth career tracks and guide me)"
            ],
            index=0 if user_interests.strip() else 1
        )

    submit_button = st.form_submit_button("Generate Personalized Career Guide & Roadmap 🚀", type="primary", use_container_width=True)

# ---------------------------------------------------------
# AI Generation & Groq Engine Execution
# ---------------------------------------------------------
if submit_button:
    if not current_field.strip():
        st.error("⚠️ Please specify your current stream or major (e.g., ICS, Pre-Engineering, BS Computer Science, etc.).")
    elif GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE" or not GROQ_API_KEY:
        st.error("⚠️ Please insert your valid Groq API Key in the code or configure it under Streamlit Secrets.")
    else:
        with st.spinner("🤖 Analyzing your academic stage, calculating career trajectories, and preparing roadmap..."):
            try:
                client = Groq(api_key=GROQ_API_KEY)

                # Prompt crafted specifically for academic stage transitions (Matric -> Inter -> BS -> Industry)
                system_prompt = """
You are a distinguished career counselor, academic advisor, and technical industry mentor with deep knowledge of education systems (including Matric, Intermediate/FSc/ICS, BS degrees, and modern global job markets).
Your role is to offer empathetic, practical, and highly actionable career guidance.

Provide output structured with clear, aesthetic Markdown headers, bullet points, and tables where suitable.
"""

                user_prompt = f"""
Student / Professional Profile:
- **Academic Milestone**: {education_stage}
- **Current Stream / Major**: {current_field}
- **Current Skill Level**: {skill_level}
- **Course / Degree they are considering**: {target_course if target_course.strip() else "None specified"}
- **Interests / Aspirations**: {user_interests if user_interests.strip() else "No specific interest mentioned. The user needs career discovery and suggestions."}
- **Exploration Mode**: {preference_mode}

Please generate a comprehensive, highly structured Career Road Guide covering:

### 1. 🎓 Next Immediate Academic / Career Milestone
- Explain what they should do next depending on whether they finished Matric (recommend suitable Intermediate groups like ICS, Pre-Eng, etc.), Intermediate (recommend top BS degree options, merit requirements, and career scope), or BS (industry tracks, internships, certifications).
- Analyze the specific course/degree they are thinking of ({target_course if target_course.strip() else 'N/A'}) and give realistic feedback on its industry value and suitability.

### 2. 🔀 Recommended Career Branches & Emergent Paths
- Provide 3 to 4 distinct modern career paths branching from their background (e.g., Technical / Software / AI, Analytical / Business / Finance, or Specialized).
- If the user has no clear interest, highlight why each suggested path is lucrative and what daily work looks like.

### 3. 🗺️ Step-by-Step Phase Roadmap (Tuned to {skill_level} Level)
- **Phase 1: Foundations (Months 1-3)**: Core fundamentals to master at their current level.
- **Phase 2: Applied Skills & Mini-Projects (Months 4-6)**: Concrete deliverables and hands-on practice.
- **Phase 3: Portfolio, Certifications & Real-World Entry (Months 7+)**: Industry preparation, GitHub/portfolio building, and job/internship readiness.

### 4. 🛠️ Tech Stack & Essential Tools
- A clear breakdown of Languages, Software/Frameworks, and Free Learning Resources (YouTube channels, documentation, practice platforms).

### 5. 🎯 7-Day Quick Start Challenge
- Concrete, actionable checklist of 3-5 tasks they should complete this upcoming week to kickstart their journey.
"""

                # Using llama-3.3-70b-versatile: free, robust, and state-of-the-art on Groq
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.6,
                    max_tokens=2500
                )

                response_text = chat_completion.choices[0].message.content

                st.success("🎉 Your Career Road Blueprint is Ready!")
                st.markdown(response_text)

                # Option to download guide
                st.download_button(
                    label="📥 Download Career Guide as Markdown",
                    data=response_text,
                    file_name=f"career_road_guide_{skill_level.lower()}.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Error generating career roadmap: {str(e)}")