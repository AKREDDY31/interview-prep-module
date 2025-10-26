# app.py
import streamlit as st
import random, json, os, uuid, time
from datetime import datetime

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Interview Preparation Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, default=str)

def append_history(record):
    h = load_history()
    h.append(record)
    save_history(h)

# ---------------------------
# Utility helpers
# ---------------------------
def normalize_text(x):
    if x is None:
        return ""
    return str(x).strip().casefold()

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
# UI CSS
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
# Start Exam
# ---------------------------
def start_exam(section, difficulty, count, total_time_minutes=30):
    qs_pool = QUESTION_BANK.get(section, {}).get(difficulty, []).copy()
    if not qs_pool:
        st.warning("No questions available for this section/difficulty.")
        return
    random.shuffle(qs_pool)
    qs = qs_pool[:count] if len(qs_pool)>=count else (qs_pool * ((count // len(qs_pool))+1))[:count]
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
        st.info("No levels available.")
        return
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        level = st.selectbox("Difficulty", levels, key=f"{section}_level")
    with col2:
        max_q = max(1, len(QUESTION_BANK.get(section, {}).get(level, [])))
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
# Results / Analytics / History
# ---------------------------
with tabs[4]:  # Results
    st.header("📈 Recent Results")
    hist = load_history()
    if not hist:
        st.info("No results yet.")
    else:
        for rec in hist[-10:][::-1]:
            section = rec.get("section","-")
            difficulty = rec.get("difficulty","-")
            score = rec.get("score",0)
            timestamp = rec.get("timestamp","-")
            st.markdown(f"**{section}** — {difficulty} | Score: **{score}** | Time: {timestamp}")

with tabs[5]:  # Analytics
    st.header("📊 Analytics")
    hist = load_history()
    if not hist:
        st.info("No data yet.")
    else:
        from collections import defaultdict
        agg = defaultdict(list)
        for r in hist:
            sec = r.get("section","-")
            s = r.get("score",0)
            agg[sec].append(s)
        cols = st.columns(len(agg))
        for c,(sec,scores) in zip(cols,agg.items()):
            with c:
                avg_score = sum(scores)/len(scores) if scores else 0
                st.metric(label=sec,value=f"{avg_score:.1f}")

with tabs[6]:  # History
    st.header("🕓 Full History")
    h = load_history()
    if not h:
        st.info("No attempts recorded.")
    else:
        for rec in h[::-1]:
            section = rec.get("section","-")
            difficulty = rec.get("difficulty","-")
            score = rec.get("score",0)
            timestamp = rec.get("timestamp","-")
            st.markdown(f"**{section}** — {difficulty} | Score: **{score}** | Time: {timestamp}")

# ---------------------------
# Exam Page (focus mode)
# ---------------------------
if st.session_state.exam:
    ex = st.session_state.exam
    st.markdown(f"<div style='padding:10px;border-radius:8px;background:#eef7ff'><b>Exam in progress:</b> {ex['section']} — {ex['difficulty']}</div>", unsafe_allow_html=True)
    
    # Live timer
    elapsed = int(time.time() - ex["start_time"])
    remaining = max(ex["duration"] - elapsed, 0)
    m,s = divmod(remaining,60)
    st.markdown(f"<h3>⏱ Time left: {m:02}:{s:02}</h3>", unsafe_allow_html=True)

    if remaining == 0:
        st.warning("Time's up — auto-submitting your answers.")
        should_submit = True
    else:
        should_submit = False

    idx = ex["idx"]
    q = ex["qs"][idx]
    st.markdown(f"<div class='q-card'><b>Q{idx+1}. {q['q']}</b></div>", unsafe_allow_html=True)

    user_key = f"answer_{idx}"
    if "options" in q and q["options"]:
        choice = st.radio("Choose an option:", q["options"], index=(q["options"].index(ex["answers"][idx]) if ex["answers"][idx] in q["options"] else 0), key=user_key)
        ex["answers"][idx] = choice
    else:
        ans = st.text_area("Your answer:", value=ex["answers"][idx], key=user_key, height=140)
        ex["answers"][idx] = ans

    # Single Save & Next button
    if st.button("💾 Save & Next"):
        if idx < len(ex["qs"])-1:
            ex["idx"] += 1
        st.session_state.exam = ex
        st.experimental_rerun()

    # Submit
    if st.button("🏁 Submit Test") or should_submit:
        correct_count = 0
        details = []
        for i_q,qobj in enumerate(ex["qs"]):
            user_ans = ex["answers"][i_q]
            correct_ans = qobj.get("a","")
            correct = is_correct(user_ans, correct_ans)
            details.append({"q": qobj.get("q"), "selected":user_ans, "correct":correct_ans, "score":1 if correct else 0})
            if correct: correct_count += 1
        score = correct_count
        rec = {
            "id": str(uuid.uuid4()),
            "section": ex["section"],
            "difficulty": ex["difficulty"],
            "timestamp": datetime.utcnow().isoformat(),
            "score": score,
            "details": details
        }
        append_history(rec)
        st.success(f"Submitted ✅ — Score: {score} / {len(ex['qs'])}")
        if score == len(ex['qs']):
            st.balloons()
        st.session_state.exam = None
        st.experimental_rerun()

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div style='text-align:center;padding:8px;color:#0b4f6c;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
