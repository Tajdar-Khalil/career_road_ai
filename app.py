import streamlit as st
import os
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

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
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

    .stTextInput > div > div > input, .stTextArea textarea, .stSelectbox > div > div {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Groq API Configuration (Key in code/secrets, never on screen)
# ---------------------------------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        GROQ_API_KEY = ""

# Fallback: paste your key directly if not using environment variables
if not GROQ_API_KEY:
    GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

# Helper function: Finds the best active non-Llama model on the account
def get_best_non_llama_model(client):
    preferred_non_llama = [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "qwen/qwen3.6-27b",
        "qwen/qwen3.8-27b",
        "gemma2-9b-it",
        "mixtral-8x7b-32768"
    ]
    try:
        available_models = [m.id for m in client.models.list().data]
        for model in preferred_non_llama:
            if model in available_models:
                return model
        # Fallback: first non-llama text model available
        for m in available_models:
            if "llama" not in m.lower() and "whisper" not in m.lower() and "guard" not in m.lower():
                return m
    except Exception:
        pass
    return "openai/gpt-oss-20b"

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Career Road")
    st.markdown("Your intelligent navigator for educational transitions, personalized roadmaps, and career growth.")
    st.markdown("---")
    
    st.markdown("#### 🎯 Supported Academic Stages:")
    st.markdown("""
    - **Matric / 10th / O-Levels** (Selecting high school/intermediate tracks: ICS, Pre-Engineering, Pre-Medical, I.Com, Arts)
    - **Intermediate / 12th / A-Levels** (University BS degrees, entry scope & requirements)
    - **Undergraduate / BS** (Specializations, practical industry tracks & certifications)
    - **Career Switcher / Self-Taught** (Fast transitions into Tech, Finance, or AI)
    """)
    st.markdown("---")
    st.markdown("Developed by Tajdar Khalil")
    st.caption("Engine: Non-Llama open architectures (`openai/gpt-oss-20b` / `qwen`)")

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🧭 Career Road: Smart AI Career Counseling & Roadmap</div>
    <div class="hero-subtitle">
        Plan your next academic or career phase with actionable milestone roadmaps, degree pathways, career branching, and essential skill stacks.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Form Section
# ---------------------------------------------------------
with st.form("career_guidance_form"):
    st.markdown("### 📋 1. Academic & Experience Profile")
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
            placeholder="e.g., ICS, Pre-Engineering, Computer Science, Commerce, Bio-Sciences, etc."
        )

    with col2:
        skill_level = st.select_slider(
            "Current Practical Skill Level *",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Beginner",
            help="Beginner: Foundations only. Intermediate: Can build independent projects. Advanced: System-level knowledge or ready for senior roles."
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
            placeholder="e.g., I enjoy problem-solving and coding, or I prefer financial markets, or 'I have no specific interest yet, please suggest high-growth fields based on market trends.'",
            height=110
        )

    with col4:
        preference_mode = st.radio(
            "Counseling Mode",
            [
                "I know my target direction (Provide deep roadmap & counseling)",
                "I am unsure / have no fixed interest (Suggest top 3 high-growth career tracks and guide me)"
            ],
            index=0 if user_interests.strip() else 1
        )

    submit_button = st.form_submit_button("Generate Personalized Career Guide & Roadmap 🚀", type="primary", use_container_width=True)

# ---------------------------------------------------------
# AI Generation Execution
# ---------------------------------------------------------
if submit_button:
    if not current_field.strip():
        st.error("⚠️ Please specify your current stream or major (e.g., ICS, Pre-Engineering, BS Computer Science, etc.).")
    elif GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE" or not GROQ_API_KEY:
        st.error("⚠️ Groq API key is missing. Set it in code or in Streamlit Secrets.")
    else:
        with st.spinner("🤖 Analyzing your academic profile and preparing roadmap..."):
            try:
                client = Groq(api_key=GROQ_API_KEY)
                selected_model = get_best_non_llama_model(client)

                system_prompt = """
You are a career counselor and technical industry mentor with deep knowledge of education structures (Matriculation, Intermediate/FSc/ICS, and Bachelor's degrees) as well as global tech and business markets.
Your goal is to provide realistic, empathetic, and actionable career guidance.
Structure your response cleanly using Markdown headings, bold keywords, and bullet points.
"""

                user_prompt = f"""
User Profile:
- Academic Milestone: {education_stage}
- Current Stream / Subjects: {current_field}
- Skill Level: {skill_level}
- Target Course/Degree Under Consideration: {target_course if target_course.strip() else "None specified"}
- Interests: {user_interests if user_interests.strip() else "No clear interest specified. Needs recommendation."}
- Counseling Mode: {preference_mode}

Please provide a detailed Career Guide covering:

1. **Immediate Academic Milestone Counseling**:
   - If after Matric: Recommend best intermediate groups (ICS, FSc Pre-Eng, Pre-Med, I.Com) and why.
   - If after Intermediate: Recommend top university BS degrees (Computer Science, Data Science, AI, Business Analytics, Finance) and prerequisites.
   - If during/after BS: Recommend industry specializations and job market readiness.
   - If they mentioned a specific course ({target_course if target_course.strip() else 'N/A'}), evaluate its current market value.

2. **Career Branches & Emergent Paths**:
   - Present 3-4 distinct career options branching from their stage.
   - If they have no clear interests, highlight why each option is high-growth and what a day in that role looks like.

3. **Phase-by-Phase Roadmap (Tailored for {skill_level} Level)**:
   - Phase 1: Core Foundations (Months 1-3)
   - Phase 2: Hands-on Projects & Practical Skills (Months 4-6)
   - Phase 3: Specialization, Portfolio & Industry Entry (Months 7+)

4. **Essential Tech Stack & Free Learning Resources**:
   - Must-learn languages, frameworks, or tools.
   - Recommended high-quality free learning platforms, documentation, and YouTube channels.

5. **7-Day Action Plan**:
   - 3 to 5 realistic tasks they should execute this week to begin.
"""

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=selected_model,
                    temperature=0.6,
                    max_tokens=2500
                )

                response_text = chat_completion.choices[0].message.content

                st.success(f"🎉 Your Career Road Blueprint is Ready! (Generated with `{selected_model}`)")
                st.markdown(response_text)

                st.download_button(
                    label="📥 Download Career Guide as Markdown",
                    data=response_text,
                    file_name="career_road_guide.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Error generating roadmap: {str(e)}")
