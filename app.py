# app.py
import streamlit as st
import random, json, os, uuid, time
from datetime import datetime

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(page_title="Interview Preparation Platform",
                   layout="wide",
                   initial_sidebar_state="expanded")

# ---------------------------
# Sidebar Instructions
# ---------------------------
st.sidebar.header("Instructions")
st.sidebar.markdown("""
- Select a section and difficulty, then click **Start Test**.
- During the exam, only the exam page is visible (focus mode).
- Use **Save & Next** to store your answer and move forward.
- Timer counts down live, second by second.
- Do not refresh the page while an attempt is active.
""")

# ---------------------------
# History helpers
# ---------------------------
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, default=str)

def append_history(record):
    hist = load_history()
    hist.append(record)
    save_history(hist)

# ---------------------------
# Utility helpers
# ---------------------------
def normalize_text(x):
    return str(x).strip().casefold() if x else ""

def is_correct(user_ans, correct_ans):
    return normalize_text(user_ans) == normalize_text(correct_ans)

# ---------------------------
# Placeholder Question Bank
# ---------------------------
QUESTION_BANK = {
    "Practice": {
        "Easy": [
            {"q": "Python function returning nothing?", "a": "None", "options":["0","None","Null","Empty"]},
            {"q": "Difference between classmethod and staticmethod?", "a": "Classmethod takes cls, staticmethod takes none", "options":["Both take self","Both take cls","Classmethod takes cls, staticmethod takes none","None"]},
        ],
        "Medium": [],
        "Hard": []
    },
    "Mock Interview": {"Easy": [], "Medium": [], "Hard": []},
    "MCQ Quiz": {"Easy": [], "Medium": [], "Hard": []},
    "Pseudocode": {"Easy": [], "Medium": [], "Hard": []},
}

# ---------------------------
# CSS for UI
# ---------------------------
st.markdown("""
<style>
.stButton>button {
  border-radius: 10px;
  padding: 10px 18px;
  font-size: 16px;
  background: linear-gradient(90deg,#4b6cb7,#182848);
  color: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.q-card {
  background: #f7fbff;
  border-radius: 10px;
  padding: 18px;
  margin-bottom: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
.stRadio > div { padding: 6px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Top header
# ---------------------------
st.markdown("<h1 style='text-align:center;color:#0b4f6c'>Interview Preparation Platform</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#0b4f6c'>Practice, Mock Interviews, MCQ Quizzes and Pseudocode exercises</h4>", unsafe_allow_html=True)

# ---------------------------
# Session State
# ---------------------------
if "exam" not in st.session_state:
    st.session_state.exam = None
if "active_section" not in st.session_state:
    st.session_state.active_section = None

# ---------------------------
# Start Exam Function
# ---------------------------
def start_exam(section, difficulty, count, total_time_minutes=30):
    qs_pool = QUESTION_BANK.get(section, {}).get(difficulty, []).copy()
    if not qs_pool:
        st.warning("No questions available for this section/difficulty.")
        return
    random.shuffle(qs_pool)
    qs = qs_pool[:count] if len(qs_pool) >= count else (qs_pool * ((count // len(qs_pool)) + 1))[:count]
    st.session_state.exam = {
        "section": section,
        "difficulty": difficulty,
        "qs": qs,
        "answers": ["" for _ in qs],
        "idx": 0,
        "start_time": time.time(),
        "duration": int(total_time_minutes*60)
    }
    st.session_state.active_section = section
    st.experimental_rerun()

# ---------------------------
# Render Section UI
# ---------------------------
def render_section_ui(section):
    st.header(f"{section}")
    levels = list(QUESTION_BANK.get(section, {}).keys())
    if not levels:
        st.info("No levels available for this section.")
        return

    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        level = st.selectbox("Difficulty", levels, key=f"{section}_level")
    with col2:
        max_q = max(0, len(QUESTION_BANK.get(section, {}).get(level, [])))
        if max_q == 0:
            st.info("No questions available in this difficulty.")
            return
        default_q = min(10, max_q)
        count = st.slider("Number of Questions", min_value=1, max_value=max_q, value=default_q, key=f"{section}_count")
    with col3:
        if st.button("▶ Start Test", key=f"{section}_start"):
            start_exam(section, level, count)
    st.write("---")
    st.write("Tips: Use the navigation button during the test. Do not refresh the page while an attempt is active.")

# ---------------------------
# Tabs for sections
# ---------------------------
tabs = st.tabs(["🧠 Practice","🎤 Mock Interview","📝 MCQ Quiz","💡 Pseudocode","📈 Results","📊 Analytics","🕓 History"])
tab_names = ["Practice","Mock Interview","MCQ Quiz","Pseudocode","Results","Analytics","History"]

# ---------------------------
# Render only if exam not active
# ---------------------------
if not st.session_state.exam:
    render_section_ui("Practice")
    render_section_ui("Mock Interview")
    render_section_ui("MCQ Quiz")
    render_section_ui("Pseudocode")

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div style='text-align:center;padding:8px;color:#0b4f6c;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
