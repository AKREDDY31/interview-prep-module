import streamlit as st
import pandas as pd
import numpy as np
import json, os, uuid, random, time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# ---- NEW: Beautiful styling ----
st.set_page_config(
    page_title="Interview Preparation Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
/* Titles / Subtitle */
.big-title {
    text-align:center;
    color:#5612c6;
    font-weight:800;
    font-size:2.8rem;
    margin-top:24px;
    margin-bottom:8px;
    letter-spacing: 0.03em;
}
.subtitle {
    text-align:center;
    color:#444B5A;
    font-size:1.2rem;
    margin-bottom:22px;
}
/* Sidebar Instructions */
.cardy {
    background: linear-gradient(120deg,#f3f5fa 60%, #e4e6fb 100%);
    border-left: 6px solid #5b21b6;
    border-radius: 16px;
    box-shadow: 0 2px 18px #2222;
    padding: 28px 18px 18px 26px;
    margin-bottom: 26px;
}
.cardy-title {
    font-size:1.23rem;
    font-weight:800;
    color:#7c3aed;
    margin-bottom:16px;
}
.cardy-li {
    font-size:1.06rem;
    color:#333;
    margin-bottom:7px !important;
    line-height:1.57em !important;
}
@media (max-width: 800px) {
    .big-title { font-size:2rem; }
    .subtitle { font-size:1.01rem; }
    .cardy { padding: 18px 10px 12px 12px; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------- Question Bank Example (expand as needed) -------------------
QUESTION_BANK = {
    "Practice": {
        "Algorithms": {
            "Easy": [{"q":"What is a stack?","a":"A stack is a linear data structure that follows LIFO."}],
            "Medium": [{"q":"Explain quicksort algorithm.","a":""}],
            "Hard": [{"q":"How does Dijkstra's algorithm work?","a":""}]
        },
        "DBMS": {
            "Easy": [{"q":"What is a primary key?","a":""}]
            # ... Populate more
        },
        # Add more topics and fill with 15 per topic/difficulty for real app
    },
    "MCQ Quiz": {
        "Python": {
            "Easy": [{"q":"Which of these is NOT a keyword?","options":["lambda","eval","pass","assert"],"a":"eval"}]
            # ... More MCQs, med, hard
        }
        # Add other MCQ topics
    },
    "Mock Interview": {
        "Technical": {
            "Easy": [{"q":"Explain OOPS concepts briefly.","a":""}]
        },
        "HR": {
            "Easy": [{"q":"Tell me about yourself.","a":""}]
        },
        # Manager/Clink, etc.
    },
    "Code Runner": {
        "Easy": [{"q":"Write a function to reverse a string. Sample input: 'hello'. Expected output: 'olleh'.\nTest Case 1: input='abc', output='cba'\nTest Case 2: input='xyz', output='zyx'","a":""}]
        # ... Populate 15 per diff
    },
    "Pseudocode": {
        "Easy": [{"q":"Write pseudocode to check if a number is even.","a":""}]
        # ... Populate 15 per diff
    }
}
TOPICS = {
    "Practice": list(QUESTION_BANK["Practice"].keys()),
    "MCQ Quiz": list(QUESTION_BANK["MCQ Quiz"].keys()),
    "Mock Interview": list(QUESTION_BANK["Mock Interview"].keys()),
    "Code Runner": ["Easy","Medium","Hard"],  # No topic, just diff for now
    "Pseudocode": ["Easy","Medium","Hard"]
}

# ----------------------- Utility Functions -------------------------------
def tfidf_similarity(a, b):
    if not a or not b or not a.strip() or not b.strip():
        return 0.0
    try:
        v = TfidfVectorizer()
        tfidf = v.fit_transform([a, b])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(min(sim * 100, 100), 2)  # cap at 100
    except:
        return 0.0

def pick_questions(section, topic, diff, count):
    try:
        pool = []
        if section in ["Practice","MCQ Quiz"]:
            pool = QUESTION_BANK[section][topic][diff].copy()
        elif section=="Mock Interview":
            pool = QUESTION_BANK["Mock Interview"][topic][diff].copy()
        elif section in ["Code Runner","Pseudocode"]:
            pool = QUESTION_BANK[section][diff]  # Assume these have only diff not topics
        random.shuffle(pool)
        # If not enough, repeat questions (for demo); in real app, enforce size
        while len(pool) < count:
            pool.append(random.choice(pool))
        return pool[:count]
    except Exception:
        return []

def load_history():
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(data):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

def record_result(section, topic, score, details):
    h = load_history()
    h.append({
        "id": str(uuid.uuid4()),
        "section": section,
        "topic": topic,
        "timestamp": datetime.utcnow().isoformat(),
        "score": round(float(score), 2) if score is not None else 0,
        "details": details
    })
    save_history(h)

# ---------------------- Sidebar Instructions & Tips ----------------------
st.sidebar.markdown("""
<div class="cardy">
<div class="cardy-title">🛠️ Instructions & Tips</div>
<ul style="padding-left:18px;margin-top:-8px;">
<li class="cardy-li">Select section, topic & difficulty, then <b>Start Test</b>.</li>
<li class="cardy-li">Timer begins after you start.</li>
<li class="cardy-li">Stay on this tab (do not switch browser tabs).</li>
<li class="cardy-li">Use Previous/Next/Save.</li>
<li class="cardy-li">Submit Test 🏁 anytime.</li>
<li class="cardy-li">Review analytics after each test.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ---------------------- Session Defaults -----------------------
if "mode" not in st.session_state:
    st.session_state.mode = "main"

# ---------------------- Main Page: Selection Tabs -----------------------
if st.session_state.mode == "main":
    st.markdown("<div class='big-title'>Interview Preparation Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Interactive Interview Practice and Analytics Portal</div>", unsafe_allow_html=True)

    section_tabs = st.tabs([
        "🧠 Practice", "🎤 Mock Interview", "📝 MCQ Quiz", "💻 Code Runner", "📄 Pseudocode",
        "📈 Results", "📊 Analytics", "🕓 History"
    ])

    # ---------- Practice Section ----------
    with section_tabs[0]:
        st.markdown("<h3 style='color:#0b7;font-size:1.2em;'>Practice</h3>", unsafe_allow_html=True)
        topic = st.selectbox("Select Topic", TOPICS["Practice"], key="practice_topic")
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="practice_diff")
        count = st.slider("Number of Questions", 1, 15, 5, key="practice_count")
        if st.button("▶ Start Practice", key="practice_start"):
            qs = pick_questions("Practice", topic, diff, count)
            st.session_state.exam = {
                "section": "Practice",
                "topic": topic,
                "diff": diff,
                "qs": qs,
                "answers": [""]*len(qs),
                "idx": 0,
                "start": time.time()
            }
            st.session_state.mode = "exam"
            st.experimental_rerun()

    # ---------- Mock Interview Section ----------
    with section_tabs[1]:
        st.markdown("<h3 style='color:#b51;font-size:1.2em;'>Mock Interview</h3>", unsafe_allow_html=True)
        interview_type = st.selectbox("Interview Type", ["Technical","HR","Manager","Clink"], key="mock_type")
        diff = st.selectbox("Difficulty", ["Easy","Medium","Hard"], key="mock_diff")
        count = st.slider("Number of Questions", 1, 15, 5, key="mock_count")
        if st.button("▶ Start Mock Interview", key="mock_start"):
            qs = pick_questions("Mock Interview", interview_type, diff, count)
            st.session_state.exam = {
                "section":"Mock Interview",
                "topic":interview_type,
                "diff":diff,
                "qs":qs,
                "answers":[""]*len(qs),
                "idx":0,
                "start":time.time()
            }
            st.session_state.mode = "exam"
            st.experimental_rerun()

    # ---------- MCQ Quiz ----------
    with section_tabs[2]:
        st.markdown("<h3 style='color:#b4006a;font-size:1.2em;'>MCQ Quiz</h3>", unsafe_allow_html=True)
        topic = st.selectbox("Quiz Topic", TOPICS["MCQ Quiz"], key="mcq_topic")
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="mcq_diff")
        count = st.slider("Number of MCQs", 1, 15, 5, key="mcq_count")
        if st.button("▶ Start MCQ Quiz", key="mcq_start"):
            qs = pick_questions("MCQ Quiz", topic, diff, count)
            st.session_state.exam = {
                "section":"MCQ Quiz",
                "topic":topic,
                "diff":diff,
                "qs":qs,
                "answers":[""]*len(qs),
                "idx":0,
                "start":time.time()
            }
            st.session_state.mode = "exam"
            st.experimental_rerun()

    # ---------- Code Runner ----------
    with section_tabs[3]:
        st.markdown("<h3 style='color:#4676fa;font-size:1.2em;'>Code Runner</h3>", unsafe_allow_html=True)
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="code_diff")
        count = st.slider("Number of Code Questions", 1, 15, 5, key="code_count")
        if st.button("▶ Start Code Practice", key="code_start"):
            qs = pick_questions("Code Runner", "", diff, count)
            st.session_state.exam = {
                "section":"Code Runner",
                "topic":"",
                "diff":diff,
                "qs":qs,
                "answers":[""]*len(qs),
                "idx":0,
                "start":time.time()
            }
            st.session_state.mode = "exam"
            st.experimental_rerun()

    # ---------- Pseudocode ----------
    with section_tabs[4]:
        st.markdown("<h3 style='color:#a555cd;font-size:1.2em;'>Pseudocode</h3>", unsafe_allow_html=True)
        diff = st.selectbox("Difficulty", ["Easy","Medium","Hard"], key="pseudo_diff")
        count = st.slider("Number of Pseudocode Questions", 1, 15, 5, key="pseudo_count")
        if st.button("▶ Start Pseudocode", key="pseudo_start"):
            qs = pick_questions("Pseudocode", "", diff, count)
            st.session_state.exam = {
                "section":"Pseudocode",
                "topic":"",
                "diff":diff,
                "qs":qs,
                "answers":[""]*len(qs),
                "idx":0,
                "start":time.time()
            }
            st.session_state.mode = "exam"
            st.experimental_rerun()

    # ---------- Results ----------
    with section_tabs[5]:
        st.subheader("📈 Results")
        h = load_history()
        if not h:
            st.info("No test results found.")
        else:
            df = pd.DataFrame(h)
            st.dataframe(df[["section","topic","timestamp","score"]])

    # ---------- Analytics ----------
    with section_tabs[6]:
        st.subheader("📊 Analytics")
        h = load_history()
        if not h:
            st.info("No data to analyze.")
        else:
            df = pd.DataFrame(h)
            if "score" in df.columns:
                fig = px.bar(df, x="section", y="score", color="section", title="Score per Section", text_auto=True)
                st.plotly_chart(fig, use_container_width=True)
                avg_scores = df.groupby("section")["score"].mean().reset_index()
                fig2 = px.pie(avg_scores, names="section", values="score", title="Strength vs Weakness")
                st.plotly_chart(fig2, use_container_width=True)

    # ---------- History ----------
    with section_tabs[7]:
        st.subheader("🕓 History")
        h = load_history()
        if not h:
            st.info("No history found.")
        else:
            for rec in h[::-1]:
                st.markdown(f"**Section:** {rec['section']} | **Topic:** {rec.get('topic','-')} | **Timestamp:** {rec['timestamp']} | **Score:** {rec['score']}")
                if st.button(f"View Details", key=rec['id']):
                    for d in rec.get("details", []):
                        st.write(f"Q: {d['q']} — Score: {d.get('score', 'N/A')}")

# ---------------------- Exam Page: Unified Logic for All Sections -----------------
elif st.session_state.mode == "exam":
    if "exam" not in st.session_state:
        st.error("No active test.")
        if st.button("Return Home"):
            st.session_state.mode = "main"
            st.experimental_rerun()
    else:
        ex = st.session_state.exam
        st.markdown(f"<h2 style='color:#4B0082;'>{ex['section']} — {ex['topic']} — Difficulty: {ex['diff']}</h2>", unsafe_allow_html=True)

        # -- Timer
        total_time = 30 * 60
        elapsed = int(time.time() - ex["start"])
        remaining = max(total_time - elapsed, 0)
        m, s = divmod(remaining, 60)
        if remaining <= 300:
            st.markdown(f"<span style='color:red;font-weight:bold;'⚠️ Time Left: {m:02}:{s:02}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:green;font-weight:bold;'>⏱ Time Left: {m:02}:{s:02}</span>", unsafe_allow_html=True)

        def calculate_and_save_results():
            details = []
            if ex["section"] in ["Practice"]:
                scores = [tfidf_similarity(a, q["a"]) for a, q in zip(ex["answers"], ex["qs"])]
                avg = np.mean(scores) if scores else 0
                details = [{"q": q["q"], "score": round(s, 2)} for q, s in zip(ex["qs"], scores)]
            elif ex["section"] == "MCQ Quiz":
                scores = []
                for a, q in zip(ex["answers"], ex["qs"]):
                    s = 1 if a == q["a"] else 0
                    scores.append(s)
                    details.append({"q": q["q"], "selected": a, "correct": q["a"], "score": s})
                avg = sum(scores)
            elif ex["section"] in ["Mock Interview","Pseudocode","Code Runner"]:
                scores = []
                for a, q in zip(ex["answers"], ex["qs"]):
                    s = tfidf_similarity(a, q["a"]) if ex["section"] != "Mock Interview" else 0.0
                    scores.append(s)
                    details.append({"q": q["q"], "answer": a, "score": s})
                avg = np.mean(scores) if scores else 0
            else:
                avg = 0
                details = [{"q": q["q"], "score": 0} for q in ex["qs"]]

            record_result(ex["section"], ex.get("topic",""), avg, details)
            del st.session_state.exam
            st.session_state.mode = "main"
            st.experimental_rerun()

        if remaining == 0:
            st.warning("⏰ Time over! Submitting...")
            calculate_and_save_results()

        # Submit button
        col1, col2 = st.columns([7, 1])
        with col2:
            if st.button("🏁 Submit Test"):
                calculate_and_save_results()

        idx = ex["idx"]
        q = ex["qs"][idx]
        st.markdown(
            f"<div style='background-color:#f9f7ff;color:#1a0441;padding:22px 15px 16px 18px;border-radius:11px;margin-bottom:12px;font-size:17.5px;font-weight:500;'><b>Q{idx+1}. {q['q']}</b></div>",
            unsafe_allow_html=True
        )

        if ex["section"] == "MCQ Quiz":
            opts = q.get("options",[])
            selected = st.radio("Select Option:", opts, index=opts.index(ex["answers"][idx]) if ex["answers"][idx] in opts else 0, key=f"ans{idx}")
            ex["answers"][idx] = selected
        elif ex["section"] == "Code Runner":
            lang = st.selectbox("Language:", ["Python","Java","C++"], key=f"lang{idx}")
            code = st.text_area("Write your code here:", value=ex["answers"][idx], height=150, key=f"ans{idx}")
            st.info("Test Cases Example:\n" + "\n".join([line for line in q["q"].splitlines() if line.lower().startswith("test case")]))
            ex["answers"][idx] = code
        else:
            ans = st.text_area("Your answer:", value=ex["answers"][idx], height=120, key=f"ans{idx}")
            ex["answers"][idx] = ans

        st.session_state.exam = ex

        f1, f2, f3 = st.columns([1, 1, 1])
        if f1.button("⬅ Previous"):
            if idx > 0:
                ex["idx"] -= 1
                st.session_state.exam = ex
                st.experimental_rerun()
        if f2.button("Next ➡"):
            if idx < len(ex["qs"]) - 1:
                ex["idx"] += 1
                st.session_state.exam = ex
                st.experimental_rerun()
        if f3.button("💾 Save Answer"):
            st.success("Answer saved ✅")

        st.progress((idx + 1) / len(ex["qs"]))
        st.caption(f"Question {idx+1}/{len(ex['qs'])}")

        time.sleep(1)
        st.experimental_rerun()

# --- Footer ---
st.markdown("<div style='text-align:center;padding:10px;color:#5612c6;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
