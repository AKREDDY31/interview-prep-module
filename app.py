# app.py
import streamlit as st
import random, json, os, uuid, time
from datetime import datetime

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(page_title="Interview Preparation Platform", layout="wide", initial_sidebar_state="expanded")

# ---------------------------
# Question bank placeholder (replace with your actual questions)
# ---------------------------
DEFAULT_BANK = {
    "Practice": {"Easy": [{"q":"Sample Q1","options":["A","B","C"],"a":"A"}]},
    "Mock Interview": {"Easy": [{"q":"Sample Q2","options":["A","B"],"a":"B"}]},
    "MCQ Quiz": {"Easy": [{"q":"Sample Q3","options":["A","B"],"a":"A"}]},
    "Pseudocode": {"Easy": [{"q":"Sample Q4","a":"Answer"}]}
}

QUESTION_BANK = DEFAULT_BANK
if os.path.exists("question_bank.json"):
    try:
        with open("question_bank.json","r",encoding="utf-8") as f:
            QUESTION_BANK = json.load(f)
    except:
        QUESTION_BANK = DEFAULT_BANK

# ---------------------------
# History helpers
# ---------------------------
HISTORY_FILE = "history.json"

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

def save_history(history):
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(history,f,indent=2,default=str)

def append_history(record):
    h = load_history()
    h.append(record)
    save_history(h)

# ---------------------------
# Utility helpers
# ---------------------------
def normalize_text(x):
    if x is None: return ""
    return str(x).strip().casefold()

def is_correct(user_ans, correct_ans):
    return normalize_text(user_ans) == normalize_text(correct_ans)

# ---------------------------
# Session state defaults
# ---------------------------
if "exam" not in st.session_state:
    st.session_state.exam = None
if "active_section" not in st.session_state:
    st.session_state.active_section = None
if "start_exam_flag" not in st.session_state:
    st.session_state.start_exam_flag = False

# ---------------------------
# UI CSS
# ---------------------------
st.markdown("""
<style>
.stButton>button {border-radius:10px;padding:10px 18px;font-size:16px;background:linear-gradient(90deg,#4b6cb7,#182848);color:white;}
.q-card {background:#f7fbff;border-radius:10px;padding:18px;margin-bottom:12px;box-shadow:0 2px 6px rgba(0,0,0,0.04);}
.stRadio>div {padding:6px 0;}
</style>
""",unsafe_allow_html=True)

# ---------------------------
# Sidebar Instructions
# ---------------------------
st.sidebar.header("📋 Instructions")
st.sidebar.markdown("""
1. Select a section and difficulty, then click **Start Test**.  
2. During the test, **focus mode** hides main tabs.  
3. Timer counts down in real-time.  
4. Use **Save & Next** to record answer and move to next question.  
5. Click **Submit Test** when done.  
6. Results will be stored and visible in **Results/Analytics/History**.
""")

# ---------------------------
# Top header + tagline
# ---------------------------
st.markdown("<h1 style='text-align:center;color:#0b4f6c'>Interview Preparation Platform</h1>",unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#1a759f'>Practice, Mock Interviews, MCQ Quizzes and Pseudocode exercises — fast and clean UI</h4>",unsafe_allow_html=True)

# ---------------------------
# Tabs
# ---------------------------
if st.session_state.exam is None:
    tabs = st.tabs(["🧠 Practice","🎤 Mock Interview","📝 MCQ Quiz","💡 Pseudocode","📈 Results","📊 Analytics","🕓 History"])
    tab_names = ["Practice","Mock Interview","MCQ Quiz","Pseudocode","Results","Analytics","History"]

# ---------------------------
# Exam functions
# ---------------------------
def start_exam(section, difficulty, count, total_time_minutes=30):
    qs_pool = QUESTION_BANK.get(section,{}).get(difficulty,[]).copy()
    if not qs_pool:
        st.warning("No questions available for chosen section/difficulty.")
        return
    random.shuffle(qs_pool)
    qs = qs_pool[:count] if len(qs_pool)>=count else (qs_pool*((count//len(qs_pool))+1))[:count]
    st.session_state.exam = {
        "section":section,
        "difficulty":difficulty,
        "qs":qs,
        "answers":["" for _ in qs],
        "idx":0,
        "start_time":time.time(),
        "duration":int(total_time_minutes*60)
    }
    st.session_state.active_section = section
    st.experimental_rerun()

# ---------------------------
# Render section UI
# ---------------------------
def render_section_ui(section, tab_index):
    if st.session_state.exam is not None: return
    with tabs[tab_index]:
        st.header(f"{section}")
        levels = list(QUESTION_BANK.get(section,{}).keys())
        if not levels:
            st.info("No levels found.")
            return
        col1,col2,col3 = st.columns([2,2,1])
        with col1:
            level = st.selectbox("Difficulty",levels,key=f"{section}_level")
        with col2:
            max_q = max(1,len(QUESTION_BANK.get(section,{}).get(level,[])))
            count = st.slider("Number of Questions",1,min(30,max_q),min(10,max_q),key=f"{section}_count")
        with col3:
            if st.button("▶ Start Test",key=f"{section}_start"):
                start_exam(section,level,count)
        st.write("---")
        st.write("Tips: Use navigation buttons during the test. Do not refresh while attempt is active.")

# ---------------------------
# Render tabs (if not in exam)
# ---------------------------
if st.session_state.exam is None:
    render_section_ui("Practice",0)
    render_section_ui("Mock Interview",1)
    render_section_ui("MCQ Quiz",2)
    render_section_ui("Pseudocode",3)

    # Results tab
    with tabs[4]:
        st.header("📈 Recent Results")
        hist = load_history()
        if not hist:
            st.info("No results yet.")
        else:
            for rec in hist[-10:][::-1]:
                sec = rec.get("section","-")
                diff = rec.get("difficulty","-")
                score = rec.get("score",0)
                ts = rec.get("timestamp","-")
                st.markdown(f"**{sec}** — {diff} | Score: **{score}** | Time: {ts}")

    # Analytics tab
    with tabs[5]:
        st.header("📊 Analytics")
        hist = load_history()
        if not hist:
            st.info("No data yet.")
        else:
            from collections import defaultdict
            agg=defaultdict(list)
            for r in hist:
                sec=r.get("section","-")
                s=r.get("score",0)
                agg[sec].append(s)
            for sec,scores in agg.items():
                avg_score = round(sum(scores)/len(scores),1) if scores else 0
                st.metric(label=sec,value=avg_score)

    # History tab
    with tabs[6]:
        st.header("🕓 Full History")
        h=load_history()
        if not h:
            st.info("No attempts recorded.")
        else:
            for rec in h[::-1]:
                sec = rec.get("section","-")
                diff = rec.get("difficulty","-")
                score = rec.get("score",0)
                ts = rec.get("timestamp","-")
                st.markdown(f"**{sec}** — {diff} | Score: **{score}** | {ts}")

# ---------------------------
# Exam rendering (focus mode)
# ---------------------------
if st.session_state.exam:
    ex = st.session_state.exam
    elapsed = int(time.time() - ex["start_time"])
    remaining = max(ex["duration"]-elapsed,0)
    m,s = divmod(remaining,60)
    st.markdown(f"<h3 style='color:#c0392b'>⏱ Time left: {m:02}:{s:02}</h3>",unsafe_allow_html=True)

    # Question
    idx = ex["idx"]
    q = ex["qs"][idx]
    st.markdown(f"<div class='q-card'><b>Q{idx+1}. {q.get('q','')}</b></div>",unsafe_allow_html=True)

    user_key=f"answer_{idx}"
    if "options" in q and q["options"]:
        choice = st.radio("Choose an option:",q["options"],index=(q["options"].index(ex["answers"][idx]) if ex["answers"][idx] in q["options"] else 0),key=user_key)
        ex["answers"][idx]=choice
    else:
        ans = st.text_area("Your answer:",value=ex["answers"][idx],key=user_key,height=140)
        ex["answers"][idx]=ans

    # Auto-save
    st.session_state.exam = ex

    # Save & Next button
    if st.button("💾 Save & Next"):
        if idx < len(ex["qs"])-1:
            ex["idx"] += 1
            st.session_state.exam = ex
            st.experimental_rerun()
        else:
            remaining=0  # auto-submit if last question

    # Submit automatically when time ends
    if remaining==0:
        correct_count=0
        details=[]
        for i_q,qobj in enumerate(ex["qs"]):
            user_ans=ex["answers"][i_q]
            correct_ans=qobj.get("a","")
            correct=is_correct(user_ans,correct_ans)
            details.append({"q":qobj.get("q","-"),"selected":user_ans,"correct":correct_ans,"score":1 if correct else 0})
            if correct: correct_count+=1

        score = correct_count
        rec={
            "id":str(uuid.uuid4()),
            "section":ex["section"],
            "difficulty":ex["difficulty"],
            "timestamp":datetime.utcnow().isoformat(),
            "score":score,
            "details":details
        }
        append_history(rec)
        st.success(f"Submitted ✅ — Score: {score} / {len(ex['qs'])}")
        if score==len(ex['qs']): st.balloons()
        st.session_state.exam=None
        st.experimental_rerun()

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div style='text-align:center;padding:8px;color:#0b4f6c;font-weight:bold;'>Developed by Anil & Team</div>",unsafe_allow_html=True)
