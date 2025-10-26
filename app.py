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
# Session state defaults
# ---------------------------
if "exam" not in st.session_state:
    st.session_state.exam = None
if "_submit_now" not in st.session_state:
    st.session_state._submit_now = False

# ---------------------------
# Question bank placeholder
# ---------------------------
DEFAULT_BANK = {
    "Practice": {"Easy": [{"q": "Sample Q1", "options": ["A", "B", "C"], "a": "A"}]},
    "Mock Interview": {"Easy": [{"q": "Sample Q2", "options": ["X", "Y", "Z"], "a": "X"}]},
    "MCQ Quiz": {"Easy": [{"q": "Sample Q3", "options": ["1", "2", "3"], "a": "1"}]},
    "Pseudocode": {"Easy": [{"q": "Sample Q4", "a": "Answer"}]}
}
QUESTION_BANK = DEFAULT_BANK
if os.path.exists("question_bank.json"):
    try:
        with open("question_bank.json", "r", encoding="utf-8") as f:
            QUESTION_BANK = json.load(f)
    except Exception:
        QUESTION_BANK = DEFAULT_BANK

# ---------------------------
# History helpers
# ---------------------------
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
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
# Utility functions
# ---------------------------
def normalize_text(x):
    if x is None:
        return ""
    return str(x).strip().casefold()

def is_correct(user_ans, correct_ans):
    return normalize_text(user_ans) == normalize_text(correct_ans)

# ---------------------------
# Sidebar instructions
# ---------------------------
st.sidebar.header("Instructions")
st.sidebar.markdown("""
- Select a section and difficulty to start a test.
- Navigate questions using Previous / Next buttons.
- Your answers are auto-saved.
- Do not refresh the page during a test.
- Submit only when done.
- Timer shows remaining time in real-time.
""")

# ---------------------------
# Top header and tagline
# ---------------------------
st.markdown("<h1 style='text-align:center;color:#0b4f6c'>Interview Preparation Platform</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#0b4f6c'>Practice, Mock Interviews, MCQ Quizzes and Pseudocode exercises</h4>", unsafe_allow_html=True)
st.write("---")

# ---------------------------
# Tabs (sections)
# ---------------------------
if not st.session_state.exam:
    tabs = st.tabs([
        "🧠 Practice",
        "🎤 Mock Interview",
        "📝 MCQ Quiz",
        "💡 Pseudocode",
        "📈 Results",
        "📊 Analytics",
        "🕓 History"
    ])
else:
    tabs = []  # hide main tabs during exam (focus mode)

# ---------------------------
# Start exam function
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
        "duration": int(total_time_minutes * 60)
    }

# ---------------------------
# Render section UI
# ---------------------------
def render_section_ui(section, tab_index):
    with tabs[tab_index]:
        st.header(f"{section}")
        levels = list(QUESTION_BANK.get(section, {}).keys())
        if not levels:
            st.info("No levels found for this section.")
            return
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            level = st.selectbox("Difficulty", levels, key=f"{section}_level")
        with col2:
            max_q = len(QUESTION_BANK.get(section, {}).get(level, []))
            max_q = max(1, max_q)
            count = st.slider("Number of Questions", 1, min(30, max_q), min(10, max_q), key=f"{section}_count")
        with col3:
            if st.button("▶ Start Test", key=f"{section}_start"):
                start_exam(section, level, count)
                st.experimental_rerun()  # safe rerun only here

        st.write("---")
        st.write("Tips: Use the navigation buttons during the test. Do not refresh the page while an attempt is active.")

# ---------------------------
# Render main tabs
# ---------------------------
if not st.session_state.exam:
    render_section_ui("Practice", 0)
    render_section_ui("Mock Interview", 1)
    render_section_ui("MCQ Quiz", 2)
    render_section_ui("Pseudocode", 3)

    # Results tab
    with tabs[4]:
        st.header("📈 Recent Results")
        hist = load_history()
        if not hist:
            st.info("No results yet.")
        else:
            for rec in hist[-10:][::-1]:
                sec = rec.get('section', '-')
                diff = rec.get('difficulty', '-')
                score = rec.get('score', 0)
                ts = rec.get('timestamp', '-')
                st.markdown(f"**{sec}** — {diff} | Score: **{score}** | Time: {ts}")

    # Analytics tab
    with tabs[5]:
        st.header("📊 Analytics")
        hist = load_history()
        if not hist:
            st.info("No data to analyze.")
        else:
            from collections import defaultdict
            agg = defaultdict(list)
            for r in hist:
                score = r.get("score")
                if isinstance(score, (int, float)):
                    agg[r.get("section", "-")].append(score)
            cols = st.columns(len(agg))
            for c, (sec, scores) in zip(cols, agg.items()):
                with c:
                    val = f"{sum(scores)/len(scores):.1f}" if scores else "0"
                    st.metric(label=sec, value=val)

    # History tab
    with tabs[6]:
        st.header("🕓 Full History")
        hist = load_history()
        if not hist:
            st.info("No attempts recorded.")
        else:
            for rec in hist[::-1]:
                sec = rec.get('section', '-')
                diff = rec.get('difficulty', '-')
                score = rec.get('score', 0)
                ts = rec.get('timestamp', '-')
                st.markdown(f"**{sec}** — {diff} | Score: **{score}** | {ts}")

# ---------------------------
# Exam page (focus mode)
# ---------------------------
if st.session_state.exam:
    ex = st.session_state.exam
    st.markdown(f"<div style='padding:10px;border-radius:8px;background:#eef7ff'><b>Exam in progress:</b> {ex['section']} — {ex['difficulty']}</div>", unsafe_allow_html=True)

    # Timer (real-time)
    elapsed = int(time.time() - ex["start_time"])
    remaining = max(ex["duration"] - elapsed, 0)
    m, s = divmod(remaining, 60)
    st.markdown(f"<h3 style='color:#d6336c'>⏱ Time left: {m:02}:{s:02}</h3>", unsafe_allow_html=True)

    # Auto-submit if time's up
    if remaining == 0:
        st.warning("Time's up — auto-submitting your answers.")
        st.session_state._submit_now = True

    # Question display
    idx = ex["idx"]
    q = ex["qs"][idx]
    st.markdown(f"<div style='padding:12px;border-radius:8px;background:#f7fbff'><b>Q{idx+1}. {q['q']}</b></div>", unsafe_allow_html=True)

    # Options / text area
    user_key = f"answer_{idx}"
    if "options" in q and q["options"]:
        choice = st.radio("Choose an option:", q["options"], index=(q["options"].index(ex["answers"][idx]) if ex["answers"][idx] in q["options"] else 0), key=user_key, horizontal=True)
        ex["answers"][idx] = choice
    else:
        ans = st.text_area("Your answer:", value=ex["answers"][idx], key=user_key, height=140)
        ex["answers"][idx] = ans

    # Navigation buttons
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        if st.button("⬅ Previous"):
            if idx > 0:
                ex["idx"] -= 1
                st.experimental_rerun()
    with c2:
        if st.button("Next ➡"):
            if idx < len(ex["qs"]) - 1:
                ex["idx"] += 1
                st.experimental_rerun()
    with c3:
        if st.button("💾 Save Answer"):
            st.success("Answer saved ✅")
    with c4:
        if st.button("🏁 Submit Test"):
            st.session_state._submit_now = True

    # Auto-save exam state
    st.session_state.exam = ex

    # Submission handling
    if st.session_state._submit_now:
        correct_count = 0
        details = []
        for i_q, qobj in enumerate(ex["qs"]):
            user_ans = ex["answers"][i_q]
            correct_ans = qobj.get("a", "")
            correct = is_correct(user_ans, correct_ans)
            details.append({
                "q": qobj.get("q"),
                "selected": user_ans,
                "correct": correct_ans,
                "score": 1 if correct else 0
            })
            if correct:
                correct_count += 1

        # Save record
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
        st.session_state._submit_now = False
        st.experimental_rerun()

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div style='text-align:center;padding:8px;color:#0b4f6c;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
