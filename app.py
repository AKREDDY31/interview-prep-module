# app.py
import streamlit as st
import random, json, os, uuid, time
from datetime import datetime
from collections import defaultdict

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
with st.sidebar:
    st.header("📋 Instructions")
    st.write("""
- Select section, difficulty, and number of questions.
- Click '▶ Start Test' to begin.
- Use ⬅ Previous / Next ➡ to navigate.
- Click 💾 Save Answer frequently (auto-save also enabled).
- Timer and progress bar auto-update every second.
- Submit test before time ends or wait for auto-submit.
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
# Placeholder question bank
# ---------------------------
DEFAULT_BANK = {
    "Practice": {"Easy": [{"q": "Sample Q1?", "options": ["A","B","C"], "a":"A"}]},
    "Mock Interview": {"Easy": [{"q": "Sample Q2?", "options": ["Yes","No"], "a":"Yes"}]},
    "MCQ Quiz": {"Easy": [{"q": "Sample Q3?", "options": ["X","Y","Z"], "a":"Z"}]},
    "Pseudocode": {"Easy": [{"q": "Write pseudocode for addition", "a":"..."}]}
}

QUESTION_BANK = DEFAULT_BANK
if os.path.exists("question_bank.json"):
    try:
        with open("question_bank.json", "r", encoding="utf-8") as f:
            QUESTION_BANK = json.load(f)
    except Exception:
        QUESTION_BANK = DEFAULT_BANK

# ---------------------------
# CSS Styling
# ---------------------------
st.markdown("""
<style>
.stButton>button {border-radius:10px;padding:10px 18px;font-size:16px;background:linear-gradient(90deg,#4b6cb7,#182848);color:white;box-shadow:0 4px 12px rgba(0,0,0,0.12);}
.q-card {background:#f7fbff;border-radius:10px;padding:18px;margin-bottom:12px;box-shadow:0 2px 6px rgba(0,0,0,0.04);}
.stRadio > div { padding:6px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header & Tagline
# ---------------------------
st.markdown("<h1 style='text-align:center;color:#0b4f6c'>Interview Preparation Platform</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#0b4f6c'>Practice, Mock Interviews, MCQ Quizzes and Pseudocode exercises — fast and clean UI.</h4>", unsafe_allow_html=True)

# ---------------------------
# Tabs / Sections
# ---------------------------
tabs = st.tabs(["🧠 Practice", "🎤 Mock Interview", "📝 MCQ Quiz", "💡 Pseudocode", "📈 Results", "📊 Analytics", "🕓 History"])
tab_names = ["Practice", "Mock Interview", "MCQ Quiz", "Pseudocode", "Results", "Analytics", "History"]

# ---------------------------
# Global states
# ---------------------------
if "exam" not in st.session_state:
    st.session_state.exam = None
if "active_section" not in st.session_state:
    st.session_state.active_section = None

# ---------------------------
# Start exam function
# ---------------------------
def start_exam(section, difficulty, count, total_time_minutes=30):
    qs_pool = QUESTION_BANK.get(section, {}).get(difficulty, []).copy()
    if not qs_pool:
        st.warning("No questions available for chosen section/difficulty.")
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
    st.rerun()

# ---------------------------
# Render Section UI
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
            start_btn = st.button("▶ Start Test", key=f"{section}_start")
        st.write("---")
        st.write("Tips: Use navigation buttons during the test. Do not refresh while test is active.")
        if start_btn:
            start_exam(section, level, count, total_time_minutes=30)

# ---------------------------
# Render tabs
# ---------------------------
for i, section in enumerate(["Practice","Mock Interview","MCQ Quiz","Pseudocode"]):
    render_section_ui(section, i)

# ---------------------------
# Results / Analytics / History
# ---------------------------
with tabs[4]:
    st.header("📈 Recent Results")
    hist = load_history()
    if not hist:
        st.info("No results yet. Take a test to see results here.")
    else:
        for rec in hist[-10:][::-1]:
            section = rec.get("section","-")
            difficulty = rec.get("difficulty","-")
            score = rec.get("score",0)
            timestamp = rec.get("timestamp","-")
            st.markdown(f"**{section}** — {difficulty} | Score: **{score}** | Time: {timestamp}")
            if st.button(f"View details {rec.get('id','')}", key=f"view_{rec.get('id','')}"):
                for d in rec.get("details", []):
                    st.write(f"- Q: {d.get('q','-')} | Ans: {d.get('selected','-')} | Correct: {d.get('correct','-')} | Score: {d.get('score',0)}")

with tabs[5]:
    st.header("📊 Analytics")
    hist = load_history()
    if not hist:
        st.info("No data to analyze yet.")
    else:
        agg = defaultdict(list)
        for r in hist:
            score = r.get('score',0)
            try:
                score = float(score)
            except:
                score = 0
            agg[r.get('section','-')].append(score)
        cols = st.columns(len(agg))
        for c, (sec, scores) in zip(cols, agg.items()):
            with c:
                numeric_scores = [s for s in scores if isinstance(s,(int,float))]
                avg = sum(numeric_scores)/len(numeric_scores) if numeric_scores else 0
                st.metric(label=sec, value=f"{avg:.1f}")

with tabs[6]:
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
            st.markdown(f"**{section}** — {difficulty} | Score: **{score}** | {timestamp}")

# ---------------------------
# Live Exam Rendering with auto-refresh timer
# ---------------------------
if st.session_state.exam:
    ex = st.session_state.exam

    # force auto-refresh every 1 second
    st_autorefresh = st.experimental_data_editor({"dummy":[0]}, num_rows="dynamic")  # hacky refresh trigger

    st.markdown(f"<div style='padding:10px;border-radius:8px;background:#eef7ff'><b>Exam in progress:</b> {ex['section']} — {ex['difficulty']}</div>", unsafe_allow_html=True)

    elapsed = int(time.time() - ex["start_time"])
    remaining = max(ex["duration"] - elapsed, 0)
    m, s = divmod(remaining, 60)
    st.markdown(f"⏱ Time left: **{m:02}:{s:02}**")
    progress_val = min(1.0, elapsed/ex["duration"]) if ex["duration"]>0 else 0
    st.progress(progress_val)

    # Auto submit when time's up
    should_submit = False
    if remaining == 0:
        should_submit = True
        st.warning("Time's up — auto-submitting your answers.")

    # Question display
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

    # Navigation buttons
    c1,c2,c3,c4 = st.columns([1,1,1,1])
    with c1:
        if st.button("⬅ Previous"):
            if idx>0:
                ex["idx"] -= 1
                st.session_state.exam = ex
                st.rerun()
    with c2:
        if st.button("Next ➡"):
            if idx<len(ex["qs"])-1:
                ex["idx"] += 1
                st.session_state.exam = ex
                st.rerun()
    with c3:
        if st.button("💾 Save Answer"):
            st.success("Answer saved ✅")
    with c4:
        if st.button("🏁 Submit Test"):
            should_submit = True

    # Auto-save after every interaction
    st.session_state.exam = ex

    # Submission
    if should_submit:
        correct_count = 0
        details = []
        for i_q,qobj in enumerate(ex["qs"]):
            user_ans = ex["answers"][i_q]
            correct_ans = qobj.get("a","")
            correct = is_correct(user_ans, correct_ans)
            details.append({
                "q": qobj.get("q"),
                "selected": user_ans,
                "correct": correct_ans,
                "score": 1 if correct else 0
            })
            if correct:
                correct_count += 1
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
        st.rerun()

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div style='text-align:center;padding:8px;color:#0b4f6c;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
