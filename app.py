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
QUESTION_FILE = "question_bank.json"

# -------------------------------
# Default Question Bank (WITH SAMPLE QUESTIONS)
# -------------------------------
# This is the sample data you requested.
# The app will use this if 'question_bank.json' is missing or empty.
DEFAULT_BANK = {
    "Practice": {
        "Aptitude": {
            "Easy": [
                {"q": "What is 15% of 200?", "a": "30"},
                {"q": "If a train travels 120 km in 3 hours, what is its average speed?", "a": "40 km/hr"}
            ],
            "Medium": [
                {"q": "A car travels 60 km/hr for 2.5 hours. How far?", "a": "150 km"}
            ],
            "Hard": [
                {"q": "Find x if 2x + 3x = 45.", "a": "9"}
            ]
        },
        "Logical Reasoning": {
            "Easy": [
                {"q": "If all cats are dogs and all dogs are lions, are all cats lions?", "a": "Yes"},
                {"q": "What comes next: 3, 6, 9, 12, ?", "a": "15"}
            ]
        }
    },
    "MCQ Quiz": {
        "Data Structures": {
            "Easy": [
                {"q": "What data structure uses LIFO?", "options": ["Queue", "Stack", "Array", "Tree"], "a": "Stack"},
                {"q": "Which is used for BFS in graphs?", "options": ["Stack", "Queue", "Heap", "List"], "a": "Queue"}
            ]
        }
    },
    "Code Runner": {
        "Easy": [
            {"q": "Write a function to return the factorial of 5.", "a": ""},
            {"q": "Write code to reverse a string 'hello'.", "a": ""}
        ],
        "Medium": [
            {"q": "Check if 'racecar' is a palindrome.", "a": ""}
        ],
        "Hard": [
             {"q": "Find the maximum subarray sum (Kadane's Algorithm).\nTest: [-2,1,-3,4,-1,2,1,-5,4] output=6", "a": ""}
        ]
    }
}

# -------------------------------
# Load Question Bank
# -------------------------------
try:
    if os.path.exists(QUESTION_FILE):
        with open(QUESTION_FILE, "r", encoding="utf-8") as f:
            QUESTION_BANK = json.load(f)
            if not QUESTION_BANK: # Check if file is empty
                st.warning(f"'{QUESTION_FILE}' is empty. Using sample questions.")
                QUESTION_BANK = DEFAULT_BANK
    else:
        st.warning(f"'{QUESTION_FILE}' not found. Using sample questions.")
        QUESTION_BANK = DEFAULT_BANK
except Exception as e:
    st.warning(f"Error loading '{QUESTION_FILE}': {e}. Using sample questions.")
    QUESTION_BANK = DEFAULT_BANK


# -------------------------------
# Helper Functions
# -------------------------------

# ✅ TF-IDF Function
def tfidf_similarity(a, b):
    """Calculates TF-IDF similarity between two strings, capped at 100."""
    if not a or not b or not a.strip() or not b.strip():
        return 0.0
    try:
        v = TfidfVectorizer()
        tfidf = v.fit_transform([a, b])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(min(sim * 100, 100), 2)  # cap at 100
    except ValueError:
        return 0.0

# ✅ CRITICAL FIX: Updated pick_questions function
def pick_questions(section, topic, difficulty, count):
    """
    Fetches questions based on the selected array values (strings).
    Handles both structures:
    - Section -> Topic -> Difficulty
    - Section -> Difficulty
    """
    section_data = QUESTION_BANK.get(section, {})
    
    # Check if this section has topics or not by looking for difficulty keys
    # This logic must match setup_test
    first_level_keys = list(section_data.keys())
    has_topics = not any(key in first_level_keys for key in ["Easy", "Medium", "Hard"])

    if has_topics:
        # Structure 1: Section -> Topic -> Difficulty
        pool = section_data.get(topic, {}).get(difficulty, []).copy()
    else:
        # Structure 2: Section -> Difficulty
        pool = section_data.get(difficulty, []).copy()

    if not pool:
        return [] # Return empty list if no questions found

    random.shuffle(pool)
    
    # Handle request for more questions than available
    original_pool = pool.copy() 
    while len(pool) < count:
        if not original_pool: break # Safety check for empty original pool
        pool.append(random.choice(original_pool)) 
        
    return pool[:count]


def load_history():
    """Loads test history from the JSON file."""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_history(data):
    """Saves test history to the JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

def record_result(section, score, details):
    """Appends a new test result to the history file."""
    h = load_history()
    h.append({
        "id": str(uuid.uuid4()),
        "section": section,
        "timestamp": datetime.utcnow().isoformat(),
        "score": round(float(score), 2) if score is not None else 0, # Handles None score for N/A
        "details": details
    })
    save_history(h)

# -------------------------------
# Sidebar Instructions
# -------------------------------
st.sidebar.title("🧭 Instructions & Tips")
st.sidebar.markdown("""
1. Select Section, Topic (if any) & Difficulty, click **Start Test**.
2. Timer starts when test begins.
3. Don’t switch tabs.
4. Use Previous | Next | Save Answer.
5. Submit Test 🏁 at any time.
6. Analytics shows strengths & weaknesses.
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

    # Define all section tabs
    all_sections = list(QUESTION_BANK.keys()) # This is your Section array [0, 1, 2, ...]
    
    # Create descriptive tab names
    tab_name_map = {
        "Practice": "🧠 Practice",
        "Mock Interview": "🎤 Mock Interview",
        "MCQ Quiz": "📊 MCQ Quiz",
        "Code Runner": "💻 Code Runner",
        "Pseudocode": "📝 Pseudocode"
    }
    # Use descriptive name if in map, otherwise default
    tab_names = [tab_name_map.get(s, f"📌 {s}") for s in all_sections]
    
    # Add permanent tabs
    tab_names.extend(["📈 Results", "📊 Performance & Analytics", "🕓 History"])
    
    section_tabs = st.tabs(tab_names)

    # ✅ CRITICAL FIX: Updated Section Generator
    def setup_test(section_name, key_prefix):
        """Creates the UI for starting a test for a given section."""
        st.markdown(f"<h3 style='color:#008080;'>{section_name}</h3>", unsafe_allow_html=True)
        
        section_data = QUESTION_BANK.get(section_name, {})
        if not section_data:
            st.warning(f"No questions found for section '{section_name}' in the question bank.")
            return

        # THIS IS THE CRITICAL LOGIC:
        # Check if the first level keys are difficulties, or topics.
        first_level_keys = list(section_data.keys())
        has_topics = True # Assume topics by default
        if not first_level_keys:
             st.error(f"No data for section: {section_name}")
             return
        
        # If any of the first keys are 'Easy', 'Medium', or 'Hard', we assume NO topics.
        if any(key in first_level_keys for key in ["Easy", "Medium", "Hard"]):
            has_topics = False
        
        topic = None
        topics_list = [] # This is the "array value to the topics"
        if has_topics:
            # This section (e.g., Practice) has topics
            topics_list = first_level_keys # This is the "array of topics" [0, 1, ...]
            if not topics_list:
                st.error(f"No topics found for section: {section_name}")
                return
            # User selects from the array, Streamlit gives us the string
            topic = st.selectbox("Select Topic", topics_list, key=f"{key_prefix}_topic")
        else:
            # This section (e.g., Code Runner) doesn't have topics
            pass 

        # This part is now safe, it runs for both structures
        difficulty_list = ["Easy", "Medium", "Hard"] # This is the "array for difficulty" [0, 1, 2]
        # User selects from the array, Streamlit gives us the string
        diff = st.selectbox("Difficulty", difficulty_list, key=f"{key_prefix}_diff")
        count = st.slider("Number of Questions", 1, 15, 5, key=f"{key_prefix}_count")
        start_btn = st.button("▶ Start Test", key=f"{key_prefix}_start")
        
        if start_btn:
            # Fetch questions based on the selected array values (strings)
            qs = pick_questions(section_name, topic, diff, count) 
            
            if not qs: # Check if pick_questions returned an empty list
                st.error(f"No questions found for {section_name} -> {topic or 'General'} -> {diff}. Please check the question bank.")
                return

            st.session_state.exam = {
                "section": section_name,
                "topic": topic if topic else "General", # Store topic
                "diff": diff,
                "qs": qs,
                "answers": [""] * len(qs),
                "idx": 0,
                "start": time.time()
            }
            st.session_state.mode = "exam"
            st.experimental_rerun()

    # ---------- Dynamically Create Tabs for Sections ----------
    for i, section_name in enumerate(all_sections):
        with section_tabs[i]:
            # Use a unique key_prefix for each section
            # section_name is the string from your "Section array"
            setup_test(section_name, section_name.lower().replace(" ", "_"))

    # ---------- Results ----------
    with section_tabs[-3]: # Corresponds to "Results"
        st.subheader("📈 Results")
        h = load_history()
        if not h:
            st.info("No test results found.")
        else:
            df = pd.DataFrame(h)
            df_display = df[["section", "timestamp", "score"]].copy()
            
            # Function to determine if a result was N/A
            def check_na(row):
                # Find the original record by index
                original_record = h[row.name]
                # Check if any detail has a score of 'N/A'
                if any(d.get('score') == 'N/A' for d in original_record.get('details', [])):
                    return "N/A (Review)"
                return row['score']

            df_display['score'] = df.apply(check_na, axis=1)
            st.dataframe(df_display, use_container_width=True)

    # ---------- Performance & Analytics ----------
    with section_tabs[-2]: # Corresponds to "Performance"
        st.subheader("📊 Performance & Analytics")
        h = load_history()
        if not h:
            st.info("No test data to analyze.")
        else:
            df = pd.DataFrame(h)
            if "score" in df.columns:
                # Filter out non-numeric scores (e.g., N/A represented as 0) for plotting
                df_numeric = df[pd.to_numeric(df['score'], errors='coerce').notnull()]
                df_numeric['score'] = df_numeric['score'].astype(float)
                
                # Exclude sections that are always N/A (score=0 and details have 'N/A')
                na_sections = set()
                for i, rec in enumerate(h):
                    if rec.get('score') == 0 and rec.get('details') and any(d.get('score') == 'N/A' for d in rec.get('details', [])):
                        na_sections.add(rec['section'])
                
                df_plottable = df_numeric[~df_numeric['section'].isin(na_sections)]

                if not df_plottable.empty:
                    fig = px.bar(df_plottable, x="section", y="score", color="section", title="Score per Section (Graded Tests)", text_auto=True)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    avg_scores = df_plottable.groupby("section")["score"].mean().reset_index()
                    fig2 = px.pie(avg_scores, names="section", values="score", title="Average Score Distribution (Graded Tests)")
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No auto-graded test data available to plot. (Mock Interviews and Code Runner are not auto-graded).")

    # ---------- History ----------
    with section_tabs[-1]: # Corresponds to "History"
        st.subheader("🕓 History")
        h = load_history()
        if not h:
            st.info("No history found.")
        else:
            for rec in h[::-1]: # Show newest first
                score_display = rec.get('score', 'N/A')
                if any(d.get('score') == 'N/A' for d in rec.get('details', [])):
                    score_display = "N/A (Review)"

                st.markdown(f"**Section:** {rec['section']} | **Timestamp:** {rec['timestamp']} | **Score:** {score_display}")
                with st.expander("View Details", expanded=False):
                    for d in rec.get("details", []):
                        st.markdown(f"**Q:** {d['q']}")
                        if 'selected' in d: # MCQ / Pseudocode
                            st.markdown(f"  - *Your Answer:* `{d['selected']}`")
                            st.markdown(f"  - *Correct Answer:* `{d['correct']}`")
                            st.markdown(f"  - *Result:* **{'Correct' if d['score'] == 1 else 'Incorrect'}**")
                        elif 'user_ans' in d: # Practice / Mock / Code
                            st.text_area("Your Answer", d['user_ans'], height=100, disabled=True, key=f"{rec['id']}_{d['q']}_user")
                            if 'correct_ans' in d: # Practice (has a correct answer)
                                st.text_area("Correct Answer", d['correct_ans'], height=50, disabled=True, key=f"{rec['id']}_{d['q']}_correct")
                            st.markdown(f"  - *Score:* **{d.get('score', 'N/A')}**")
                        st.divider()

# -------------------------------
# EXAM PAGE
# -------------------------------
elif st.session_state.mode == "exam":
    if "exam" not in st.session_state:
        st.error("No active test found.")
        if st.button("Return Home"):
            st.session_state.mode = "main"
            st.experimental_rerun()
    else:
        ex = st.session_state.exam
        st.markdown(f"<h2 style='color:#4B0082;'>{ex['section']} (Topic: {ex['topic']}) — Difficulty: {ex['diff']}</h2>", unsafe_allow_html=True)

        # ----- Timer -----
        total_time = 30 * 60 # 30 minutes
        elapsed = int(time.time() - ex["start"])
        remaining = max(total_time - elapsed, 0)
        m, s = divmod(remaining, 60)
        
        timer_placeholder = st.empty()
        if remaining <= 300: # 5 minutes
            timer_placeholder.markdown(f"<h3 style='color:red;font-weight:bold;'>⚠️ Time Left: {m:02}:{s:02}</h3>", unsafe_allow_html=True)
        else:
            timer_placeholder.markdown(f"<h3 style='color:green;font-weight:bold;'>⏱ Time Left: {m:02}:{s:02}</h3>", unsafe_allow_html=True)

        # ✅ Updated Score Calculation
        def calculate_and_save_results():
            details = []
            avg = 0
            scores = []
            
            # Sections with simple, text-based answers (Practice)
            if ex["section"] == "Practice":
                scores = [tfidf_similarity(a, q["a"]) for a, q in zip(ex["answers"], ex["qs"])]
                avg = np.mean(scores) if scores else 0
                details = [{"q": q["q"], "user_ans": a, "correct_ans": q["a"], "score": round(s, 2)} for a, q, s in zip(ex["answers"], ex["qs"], scores)]
            
            # Sections with multiple-choice answers (MCQ, Pseudocode)
            elif ex["section"] in ["MCQ Quiz", "Pseudocode"]:
                for a, q in zip(ex["answers"], ex["qs"]):
                    s = 1 if str(a).strip() == str(q["a"]).strip() else 0 # Compare as strings
                    scores.append(s)
                    details.append({"q": q["q"], "selected": a, "correct": q["a"], "score": s})
                # Score is total correct answers
                avg = sum(scores) 
            
            # Sections with no auto-grading (Mock Interview, Code Runner)
            else:
                avg = 0 # Store as 0, but use 'N/A' in details
                details = [{"q": q["q"], "user_ans": a, "score": "N/A"} for a, q in zip(ex["answers"], ex["qs"])]

            record_result(ex["section"], avg, details)
            st.success("Test Submitted Successfully!")
            st.balloons()
            del st.session_state.exam
            st.session_state.mode = "main"
            time.sleep(2) # Pause to show success
            st.experimental_rerun()

        # Auto-submit
        if remaining == 0:
            st.warning("⏰ Time over! Auto-submitting...")
            time.sleep(2) # Give user time to see message
            calculate_and_save_results()
            st.experimental_rerun() # Ensure it reruns to go to main page

        # Submit button
        col1, col2 = st.columns([8, 1])
        with col2:
            if st.button("🏁 Submit Test"):
                calculate_and_save_results()

        # Question display
        idx = ex["idx"]
        q = ex["qs"][idx]
        st.markdown(
            f"<div style='background-color:#F0F8FF;color:#000000;padding:20px;border-radius:10px;margin-bottom:15px;font-size:18px;'><b>Q{idx+1}. {q['q']}</b></div>",
            unsafe_allow_html=True
        )

        # Answer Input
        if ex["section"] in ["MCQ Quiz", "Pseudocode"]:
            options = q.get("options", [])
            current_answer = ex["answers"][idx]
            
            # Normalize options and answer for comparison
            normalized_options = [str(opt).strip() for opt in options]
            normalized_answer = str(current_answer).strip()
            
            # Use the string from the options array to display
            display_options = q.get("options", [])
            
            try:
                default_index = normalized_options.index(normalized_answer)
            except ValueError:
                default_index = 0 # Default to first option if answer not set
                if current_answer == "": # Set initial answer to first option
                    ex["answers"][idx] = display_options[0] if display_options else ""
            
            # Use the original options (with formatting) for display
            selected = st.radio("Select Option:", display_options, index=default_index, key=f"ans{idx}")
            ex["answers"][idx] = selected

        elif ex["section"] == "Code Runner":
            ans = st.text_area("Write code here:", value=ex["answers"][idx], height=250, key=f"ans{idx}")
            ex["answers"][idx] = ans
        else: # Practice, Mock Interview
            ans = st.text_area("Your answer:", value=ex["answers"][idx], height=200, key=f"ans{idx}")
            ex["answers"][idx] = ans

        st.session_state.exam = ex

        # Navigation Buttons
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
            # Answer is already saved on input change, this just provides user feedback
            st.success("Answer saved ✅")

        st.progress((idx + 1) / len(ex["qs"]))
        st.caption(f"Question {idx+1}/{len(ex['qs'])}")

        # Rerun to update timer
        if remaining > 0:
            time.sleep(1)
            st.experimental_rerun()

# -------------------------------
# Footer
# -------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;padding:10px;color:#4B0082;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
