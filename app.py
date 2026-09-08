import streamlit as st
import os
import re
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
    
    /* Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 2.2rem 2rem;
        margin-bottom: 1.5rem;
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
    
    /* Quick Pill Styling */
    .preset-pill {
        display: inline-block;
        padding: 4px 12px;
        margin: 2px 4px;
        border-radius: 14px;
        background-color: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        font-size: 0.82rem;
        cursor: pointer;
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

# Helper function: Finds the best active non-Llama model on your account
def get_best_non_llama_model(client):
    preferred_non_llama = [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "qwen/qwen3.6-27b",
        "qwen/qwen3.8-27b"
    ]
    try:
        available_models = [m.id for m in client.models.list().data]
        for model in preferred_non_llama:
            if model in available_models:
                return model
        for m in available_models:
            m_lower = m.lower()
            if "llama" not in m_lower and "whisper" not in m_lower and "guard" not in m_lower:
                return m
    except Exception:
        pass
    return "openai/gpt-oss-20b"

# ---------------------------------------------------------
# Session State Initialization (Fixes Rerun & Vanishing Bug)
# ---------------------------------------------------------
if "guide_output" not in st.session_state:
    st.session_state["guide_output"] = None
if "selected_model_used" not in st.session_state:
    st.session_state["selected_model_used"] = None
if "preset_field_value" not in st.session_state:
    st.session_state["preset_field_value"] = ""

def set_field_value(val):
    st.session_state["preset_field_value"] = val

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Career Road")
    st.markdown("Your personalized career navigation engine.")
    st.markdown("---")
    
    st.markdown("#### 🎯 Smart Stage Progression:")
    st.markdown("""
    - **Matric / 10th:** Direct guidance on Intermediate groups (ICS, Pre-Eng, Pre-Med, I.Com).
    - **Intermediate / 12th:** Direct guidance on University BS degrees and entry criteria (does not repeat Matric).
    - **Undergraduate / BS:** Direct guidance on industry roles, skills, internships, and certifications (does not repeat schooling).
    """)
    st.markdown("---")
    st.caption("Engine: Non-Llama open architectures (`openai/gpt-oss-20b` / `qwen`)")

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🧭 Career Road: Smart AI Career Counseling & Roadmap</div>
    <div class="hero-subtitle">
        Get tailored, milestone-based career counseling and practical roadmaps starting strictly from your current level without unnecessary repetition.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Form Section - Clean Inputs & Stage Adaptations
# ---------------------------------------------------------
# Quick helper chips above the form
st.markdown("##### ⚡ Quick Select Stream / Major (Click to fill):")
chip_col1, chip_col2, chip_col3, chip_col4, chip_col5, chip_col6 = st.columns(6)
with chip_col1:
    if st.button("ICS (Computer)", use_container_width=True):
        st.session_state["preset_field_value"] = "ICS (Computer Science)"
with chip_col2:
    if st.button("FSc Pre-Eng", use_container_width=True):
        st.session_state["preset_field_value"] = "FSc Pre-Engineering"
with chip_col3:
    if st.button("FSc Pre-Med", use_container_width=True):
        st.session_state["preset_field_value"] = "FSc Pre-Medical"
with chip_col4:
    if st.button("BS Comp Science", use_container_width=True):
        st.session_state["preset_field_value"] = "BS Computer Science"
with chip_col5:
    if st.button("BS Data Science", use_container_width=True):
        st.session_state["preset_field_value"] = "BS Data Science"
with chip_col6:
    if st.button("BBA / Finance", use_container_width=True):
        st.session_state["preset_field_value"] = "BBA / Finance"

with st.form("career_guidance_form"):
    st.markdown("### 📋 1. Academic & Experience Profile")
    col1, col2 = st.columns([1, 1])

    with col1:
        education_stage = st.selectbox(
            "Current Academic Stage *",
            options=[
                "Matric / 10th / O-Levels",
                "Intermediate / 12th / A-Levels",
                "Undergraduate (Enrolled in BS)",
                "Graduate (BS / Master's Completed)",
                "Career Switcher / Self-Taught"
            ],
            index=1,
            help="Select your current milestone or highest completed level."
        )

        current_field = st.text_input(
            "Current Education / Stream / Major *",
            value=st.session_state["preset_field_value"],
            placeholder="Please enter your education"
        )

    with col2:
        skill_level = st.select_slider(
            "Current Practical Skill Level *",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Beginner",
            help="Beginner: Just starting. Intermediate: Can build projects. Advanced: System-level experience."
        )

        target_course = st.text_input(
            "Target Course or Degree (Optional)",
            placeholder="Please enter the specific course or degree you are considering"
        )

    st.markdown("### 💡 2. Interests & Career Direction")
    col3, col4 = st.columns([1, 1])

    with col3:
        user_interests = st.text_area(
            "Interests, Hobbies, or Domains (Optional)",
            placeholder="Please enter your interests or preferred fields",
            height=100
        )

    with col4:
        preference_mode = st.radio(
            "Counseling Mode",
            [
                "I know my target direction (Provide deep roadmap & counseling)",
                "I am unsure / have no fixed interest (Suggest top high-growth career tracks and guide me)"
            ],
            index=0 if user_interests.strip() else 1
        )

    submit_button = st.form_submit_button("Generate Personalized Career Guide & Roadmap 🚀", type="primary", use_container_width=True)

# ---------------------------------------------------------
# AI Generation Execution
# ---------------------------------------------------------
if submit_button:
    if not current_field.strip():
        st.error("⚠️ Please enter your education in the stream/major field.")
    elif GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE" or not GROQ_API_KEY:
        st.error("⚠️ Groq API key is missing. Set it in code or in Streamlit Secrets.")
    else:
        # Strict stage routing rules
        if "Matric" in education_stage:
            stage_instruction = """
STAGE INSTRUCTION: The user is at the Matric / 10th / O-Levels milestone.
- Focus STRICTLY on the immediate next step: Choosing an Intermediate group (e.g., ICS, FSc Pre-Engineering, FSc Pre-Medical, I.Com, FA, or Technical Diplomas).
- Detail the core subjects, the university degrees each group unlocks, and which intermediate group fits their profile.
- DO NOT skip ahead to senior industry certifications; focus on laying strong academic foundations in Intermediate.
"""
        elif "Intermediate" in education_stage:
            stage_instruction = """
STAGE INSTRUCTION: The user is at the Intermediate / 12th / A-Levels milestone.
- DO NOT start over from Matric. DO NOT recommend Intermediate groups (they already passed that).
- Focus STRICTLY on what to do after Intermediate: Choosing university BS degrees (e.g., BS Computer Science, BS Software Engineering, BS Data Science, BBA/BS Finance, Engineering disciplines, etc.).
- Discuss university entrance exams, merit criteria, and high-demand university programs.
"""
        elif "Undergraduate" in education_stage:
            stage_instruction = """
STAGE INSTRUCTION: The user is currently enrolled in an Undergraduate (BS) degree.
- DO NOT start over from Matric or Intermediate. That is past history.
- Focus STRICTLY on: Semester-wise skill building, choosing high-impact electives, building real-world projects/GitHub, landing internships, and preparing for final-year projects and post-graduation job markets.
"""
        elif "Graduate" in education_stage:
            stage_instruction = """
STAGE INSTRUCTION: The user has completed their BS / Master's degree.
- DO NOT start over from school milestones.
- Focus STRICTLY on: Direct job market entry, industry roles, technical portfolio readiness, high-value professional certifications, and postgraduate paths (MS/MPhil/Abroad) if applicable.
"""
        else:
            stage_instruction = """
STAGE INSTRUCTION: The user is a career switcher or self-taught learner.
- Focus strictly on industry skills, practical project portfolios, skill bridges, and immediate market entry without traditional schooling prerequisites.
"""

        system_prompt = f"""
You are an expert career counselor and academic mentor.
{stage_instruction}

CRITICAL RULES:
1. Always respect the user's current milestone. NEVER start over from a milestone the user has already passed.
2. Structure your response cleanly using aesthetic Markdown headers, bold highlights, and actionable lists.
3. If the user provided no specific interest or is unsure, provide 3 well-explained career paths emerging directly from their current stage.
"""

        user_prompt = f"""
User Profile:
- Academic Milestone: {education_stage}
- Current Education / Major: {current_field}
- Practical Skill Level: {skill_level}
- Target Course/Degree Under Consideration: {target_course if target_course.strip() else "None specified (Suggest the best fit)"}
- Interests: {user_interests if user_interests.strip() else "No clear interest specified. Needs recommendation."}
- Counseling Mode: {preference_mode}

Please provide a structured Career Road Guide containing:

### 1. 🎓 Next Immediate Path & Counseling (Starting directly from their current stage)
- Address their current stage directly without repeating completed schooling.
- If they mentioned a specific target course/degree ({target_course if target_course.strip() else 'N/A'}), evaluate its industry demand and suitability.

### 2. 🔀 Recommended Career Branches & Emergent Tracks
- Provide 3 distinct forward-looking paths emerging from their current point.
- Detail what daily work looks like in each field and the career growth potential.

### 3. 🗺️ Step-by-Step Roadmap (Tailored for {skill_level} Level)
- Phase 1: Core Foundations (Months 1-3)
- Phase 2: Hands-on Projects & Practical Skills (Months 4-6)
- Phase 3: Specialization, Portfolio & Market Entry (Months 7+)

### 4. 🛠️ Tech Stack, Tools & Free Learning Resources
- Recommended tools, software, or programming languages relevant to their next steps.
- High-quality free learning resources (documentation, YouTube channels, practice sites).

### 5. 🎯 7-Day Action Plan
- 3 to 5 concrete tasks to get started this upcoming week.
"""

        with st.spinner("🤖 Consulting career benchmarks and preparing your roadmap..."):
            try:
                client = Groq(api_key=GROQ_API_KEY)
                selected_model = get_best_non_llama_model(client)

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
                # Save into session state
                st.session_state["guide_output"] = response_text
                st.session_state["selected_model_used"] = selected_model

            except Exception as e:
                st.error(f"Error generating roadmap: {str(e)}")

# ---------------------------------------------------------
# Display Generated Guide (Persistent via Session State)
# ---------------------------------------------------------
if st.session_state["guide_output"]:
    st.markdown("---")
    st.success(f"🎉 Your Career Road Blueprint is Ready! (Generated with `{st.session_state['selected_model_used']}`)")

    content = st.session_state["guide_output"]

    # Interactive tabs for mobile scannability and clean layout
    view_mode = st.radio("Choose Display Format:", ["📑 Tabbed Sections", "📜 Full Single Page"], horizontal=True)

    if view_mode == "📜 Full Single Page":
        st.markdown(content)
    else:
        # Split markdown by top level section numbers
        sections = re.split(r'(?=###\s+\d+\.)', content)
        
        tab_titles = [
            "🎓 Next Immediate Path",
            "🔀 Career Branches",
            "🗺️ Step Roadmap",
            "🛠️ Tech & Tools",
            "🎯 7-Day Plan"
        ]
        
        tabs = st.tabs(tab_titles)
        
        # If successfully split into 5+ sections (preamble + 5 sections)
        if len(sections) >= 6:
            for idx, tab in enumerate(tabs):
                with tab:
                    st.markdown(sections[idx + 1])
        elif len(sections) > 1:
            for idx, section in enumerate(sections[1:]):
                if idx < len(tabs):
                    with tabs[idx]:
                        st.markdown(section)
        else:
            st.markdown(content)

    st.download_button(
        label="📥 Download Career Guide as Markdown",
        data=st.session_state["guide_output"],
        file_name="career_road_guide.md",
        mime="text/markdown",
        use_container_width=True
    )