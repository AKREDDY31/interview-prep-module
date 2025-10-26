# app.py
import streamlit as st
import pandas as pd
import numpy as np
import json, os, uuid, random, time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Interview Preparation Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Files
# -------------------------------
HISTORY_FILE = "history.json"

# -------------------------------
# Default Question Bank
# -------------------------------
DEFAULT_BANK = {
    "Practice": {
        "Easy": [
            {"q": "What is the time complexity of accessing an element in a list by index?", 
             "a": "O(1)", "options": ["O(n)", "O(log n)", "O(1)", "O(n^2)"]},
            {"q": "What does 'len()' function do in Python?", 
             "a": "Returns length", "options": ["Calculates mean", "Returns length", "Finds maximum", "Counts spaces"]}
        ],
        "Medium": [],
        "Hard": []
    },
    "Mock Interview": {
        "Easy": [{"q": "Explain OOP concepts briefly.", "a": "Encapsulation, Inheritance, Polymorphism, Abstraction"}],
        "Medium": [],
        "Hard": []
    },
    "MCQ Quiz": {
        "Easy": [
            {"q": "Which keyword is used to define a function in Python?", 
             "a": "def", "options": ["func", "define", "def", "lambda"]},
            {"q": "Which data structure uses FIFO?", 
             "a": "Queue", "options": ["Stack", "Queue", "List", "Tree"]}
        ],
        "Medium": [],
        "Hard": []
    },
    "Pseudocode": {
        "Easy": [
            {"q": "If a > b then print a else print b", "a": "Compares two numbers", 
             "options": ["Addition", "Comparison", "Looping", "None"]}
        ],
        "Medium": [],
        "Hard": []
    }
}

# -------------------------------
# Load Question Bank
# -------------------------------
try:
    if os.path.exists("question_bank.json"):
        with open("question_bank.json", "r", encoding="utf-8") as f:
            QUESTION_BANK = json.load(f)
    else:
        QUESTION_BANK = DEFAULT_BANK
except:
    QUESTION_BANK = DEFAULT_BANK

# -------------------------------
# Helper Functions
# -------------------------------
def tfidf_similarity(a, b):
    if not a or not b or not a.strip() or not b.strip():
        return 0.0
    try:
        v = TfidfVectorizer()
        tfidf = v.fit_transform([a, b])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(min(sim * 100, 100), 2)
    except ValueError:
        return 0.0

def pick_questions(section, difficulty, count):
    pool = QUESTION_BANK.get(section, {}).get(difficulty, []).copy()
    random.shuffle(pool)
    while len(pool) < count and pool:
        pool.append(random.choice(pool))
    return pool[:count]

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

def record_result(section, score, details):
    h = load_history()
    h.append({
        "id": str(uuid.uuid4()),
        "section": section,
        "timestamp": datetime.utcnow().isoformat(),
        "score": round(float(score), 2) if score is not None else 0,
        "details": details
    })
    save_history(h)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🧭 Instructions & Tips")
st.sidebar.markdown("""
1. Select Section & Difficulty, click **Start Test**.  
2. Timer starts when test begins.  
3. Don’t switch tabs.  
4. Use Previous | Next | Save Answer.  
5. Submit Test 🏁 any time.  
6. View Results & Analytics after completion.
""")

# -------------------------------
# Session State Defaults
# -------------------------------
if "mode" not in st.session_state:
    st.session_state.mode = "main"

# -------------------------------
# MAIN PAGE
# -------------------------------
if st.session_state.mode == "main":
    st.markdown("<h1 style='text-align:center;color:#4B0082;'>Interview Preparation Platform</h1>", unsafe_allow_html=True)
    st.write("Interactive Interview Practice and Analytics Portal")

    section_tabs = st.tabs([
        "🧠 Practice", "🎤 Mock Interview", "📝 MCQ Quiz", "💡 Pseudocode",
        "📈 Results", "📊 Performance & Analytics", "🕓 History"
    ])

    # ---------- Section Setup ----------
    def setup_test(section_name, key_prefix):
        st.markdown(f"<h3 style='color:#008080;'>{section_name}</h3>", unsafe_allow_html=True)
        topic = st.selectbox("Select Topic", ["Practice"], key=f"{key_prefix}_topic")
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key=f"{key_prefix}_diff")
        count = st.slider("Number of Questions", 1, 15, 5, key=f"{key_prefix}_count")
        start_btn = st.button("▶ Start Test", key=f"{key_prefix}_start")
        if start_btn:
            qs = pick_questions(section_name, diff, count)
            st.session_state.exam = {
                "section": section_name,
                "topics": [topic],
                "diff": diff,
                "qs": qs,
                "answers": [""] * len(qs),
                "idx": 0,
                "start": time.time()
            }
            st.session_state.mode = "exam"
            st.rerun()

    # ---------- Tabs ----------
    with section_tabs[0]: setup_test("Practice", "practice")
    with section_tabs[1]: setup_test("Mock Interview", "mock")
    with section_tabs[2]: setup_test("MCQ Quiz", "mcq")
    with section_tabs[3]: setup_test("Pseudocode", "pseudo")

    # ---------- Results ----------
    with section_tabs[4]:
        st.subheader("📈 Results")
        h = load_history()
        if not h:
            st.info("No test results found.")
        else:
            df = pd.DataFrame(h)
            df_display = df[["section", "timestamp", "score"]].copy()
            st.dataframe(df_display)

    # ---------- Performance ----------
    with section_tabs[5]:
        st.subheader("📊 Performance & Analytics")
        h = load_history()
        if not h:
            st.info("No test data to analyze.")
        else:
            df = pd.DataFrame(h)
            if "score" in df.columns:
                fig = px.bar(df, x="section", y="score", color="section", title="Score per Section", text_auto=True)
                st.plotly_chart(fig, use_container_width=True)
                avg_scores = df.groupby("section")["score"].mean().reset_index()
                fig2 = px.pie(avg_scores, names="section", values="score", title="Strength vs Weakness")
                st.plotly_chart(fig2, use_container_width=True)

    # ---------- History ----------
    with section_tabs[6]:
        st.subheader("🕓 History")
        h = load_history()
        if not h:
            st.info("No history found.")
        else:
            for rec in h[::-1]:
                st.markdown(f"**Section:** {rec['section']} | **Timestamp:** {rec['timestamp']} | **Score:** {rec['score']}")
                if st.button(f"View Details {rec['id']}", key=rec['id']):
                    for d in rec.get("details", []):
                        st.write(f"Q: {d['q']} — Score: {d.get('score', 'N/A')}")

# -------------------------------
# EXAM PAGE
# -------------------------------
elif st.session_state.mode == "exam":
    if "exam" not in st.session_state:
        st.error("No active test.")
        if st.button("Return Home"):
            st.session_state.mode = "main"
            st.rerun()
    else:
        ex = st.session_state.exam
        st.markdown(f"<h2 style='color:#4B0082;'>{ex['section']} — Difficulty: {ex['diff']}</h2>", unsafe_allow_html=True)

        # Timer
        total_time = 30 * 60
        elapsed = int(time.time() - ex["start"])
        remaining = max(total_time - elapsed, 0)
        m, s = divmod(remaining, 60)
        color = "red" if remaining <= 300 else "green"
        st.markdown(f"<span style='color:{color};font-weight:bold;'>⏱ Time Left: {m:02}:{s:02}</span>", unsafe_allow_html=True)

        # Result Save
        def calculate_and_save_results():
            details = []
            if ex["section"] in ["Practice", "Mock Interview"]:
                scores = [tfidf_similarity(a, q["a"]) for a, q in zip(ex["answers"], ex["qs"])]
                avg = np.mean(scores) if scores else 0
                details = [{"q": q["q"], "score": round(s, 2)} for q, s in zip(ex["qs"], scores)]
            elif ex["section"] in ["MCQ Quiz", "Pseudocode"]:
                scores = [1 if a == q["a"] else 0 for a, q in zip(ex["answers"], ex["qs"])]
                avg = sum(scores)
                details = [{"q": q["q"], "selected": a, "correct": q["a"], "score": s} for q, a, s in zip(ex["qs"], ex["answers"], scores)]
            else:
                avg = 0
                details = [{"q": q["q"], "score": 0} for q in ex["qs"]]

            record_result(ex["section"], avg, details)
            del st.session_state.exam
            st.session_state.mode = "main"
            st.rerun()

        # Auto-submit
        if remaining == 0:
            st.warning("⏰ Time over! Auto-submitting...")
            calculate_and_save_results()

        # Submit button
        if st.button("🏁 Submit Test"):
            calculate_and_save_results()

        # Question display
        idx = ex["idx"]
        q = ex["qs"][idx]
        st.markdown(
            f"<div style='background-color:#F0F8FF;color:#000000;padding:20px;border-radius:10px;margin-bottom:15px;font-size:18px;'><b>Q{idx+1}. {q['q']}</b></div>",
            unsafe_allow_html=True
        )

        if ex["section"] in ["MCQ Quiz", "Pseudocode"]:
            selected = st.radio("Select Option:", q.get("options", []), key=f"ans{idx}")
            ex["answers"][idx] = selected
        else:
            ans = st.text_area("Your answer:", value=ex["answers"][idx], height=150, key=f"ans{idx}")
            ex["answers"][idx] = ans

        st.session_state.exam = ex

        # Navigation Buttons
        f1, f2, f3 = st.columns([1, 1, 1])
        if f1.button("⬅ Previous"):
            if idx > 0:
                ex["idx"] -= 1
                st.session_state.exam = ex
                st.rerun()
        if f2.button("Next ➡"):
            if idx < len(ex["qs"]) - 1:
                ex["idx"] += 1
                st.session_state.exam = ex
                st.rerun()
        if f3.button("💾 Save Answer"):
            st.success("Answer saved ✅")

        st.progress((idx + 1) / len(ex["qs"]))
        st.caption(f"Question {idx+1}/{len(ex['qs'])}")

# -------------------------------
# Footer
# -------------------------------
st.markdown("<div style='text-align:center;padding:10px;color:#4B0082;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
