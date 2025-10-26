# app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import plotly.graph_objects as go
from streamlit_extras.let_it_rain import rain  # For confetti effect

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Interview Preparation Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# CSS for Futuristic UI
# -------------------------------
st.markdown("""
<style>
/* Glass Panels & Background */
.stApp {
    background: linear-gradient(135deg, #d9e2ec, #f0f4f8);
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
}

/* Main content glass */
.css-18e3th9 {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    animation: fadeIn 0.8s ease-in-out;
}

/* Fade-in Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px);}
    to { opacity: 1; transform: translateY(0);}
}

/* Button Hover Effects */
.stButton>button {
    background-color: #0055a5;
    color: white;
    border-radius: 12px;
    padding: 0.5em 1.5em;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #003366;
    transform: scale(1.05);
}

/* Radio Hover */
.stRadio>div>label:hover {
    color: #0055a5;
    font-weight: 600;
}

/* Question Card */
.question-card {
    padding: 18px;
    border-radius: 18px;
    background: rgba(0, 85, 165, 0.08);
    margin-bottom: 15px;
    transition: all 0.3s ease;
}
.question-card:hover {
    background: rgba(0, 85, 165, 0.15);
}

/* Selected answer highlight */
.selected-answer {
    background-color: rgba(0,85,165,0.2);
    border-radius: 10px;
}

/* Badge glow animation */
.badge {
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: bold;
    color: white;
    text-align: center;
    animation: glow 1.5s infinite alternate;
    margin: 10px 0;
}
.gold { background: #FFD700; }
.silver { background: #C0C0C0; }
.bronze { background: #CD7F32; }

@keyframes glow {
    from { box-shadow: 0 0 5px #fff; }
    to { box-shadow: 0 0 20px #0055a5; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Initialize Session State
# -------------------------------
if "section" not in st.session_state:
    st.session_state.section = "Practice"
if "results" not in st.session_state:
    st.session_state.results = []
if "in_test" not in st.session_state:
    st.session_state.in_test = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = []
if "score" not in st.session_state:
    st.session_state.score = 0

# -------------------------------
# Placeholder Question Bank
# -------------------------------
question_bank = {}  # Add your questions here

# -------------------------------
# Sidebar Navigation & Instructions
# -------------------------------
st.sidebar.title("📘 Navigation")
section = st.sidebar.radio(
    "Choose Section",
    ["Practice", "Mock Interview", "MCQ Quiz", "Pseudocode", "Results", "Analytics", "History"],
    index=["Practice", "Mock Interview", "MCQ Quiz", "Pseudocode", "Results", "Analytics", "History"].index(st.session_state.section)
)
st.session_state.section = section

st.sidebar.markdown("---")
st.sidebar.title("🧭 Instructions")
st.sidebar.info("""
**Guidelines:**
- Select a section to begin practice.  
- Do **not refresh** during a test.  
- Navigate smoothly using sidebar options.  
- Results and analytics saved automatically.  
- Enjoy a futuristic interactive experience.
""")

# -------------------------------
# Header
# -------------------------------
st.markdown("""
<h1 style='text-align:center; color:#003366; font-weight:800;'>
    Interview Preparation Platform
</h1>
<hr style='border: 2px solid #003366; width: 60%; margin:auto; border-radius:5px;'>
""", unsafe_allow_html=True)
st.write("### Practice, Mock Interviews, MCQ Quizzes and Pseudocode — modern interactive UI with futuristic features.")

# -------------------------------
# Section: Practice
# -------------------------------
if section == "Practice":
    st.subheader("🧩 Practice")
    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
    num_q = st.slider("Number of Questions", 1, 20, 10)
    start = st.button("🚀 Start Test")

    if start:
        if difficulty not in question_bank or len(question_bank[difficulty]) == 0:
            st.warning("⚠️ No questions found. Add questions to `question_bank` first.")
        else:
            st.session_state.in_test = True
            st.session_state.current_question = 0
            st.session_state.selected_answers = []
            st.session_state.score = 0
            st.session_state.questions = random.sample(
                question_bank[difficulty],
                min(num_q, len(question_bank[difficulty]))
            )
            st.rerun()

    if st.session_state.in_test:
        q_idx = st.session_state.current_question
        q_data = st.session_state.questions[q_idx]

        # Question Card
        st.markdown(f"<div class='question-card'><b>Q{q_idx+1}:</b> {q_data['q']}</div>", unsafe_allow_html=True)

        # Radio Options
        choice = st.radio("Select your answer:", q_data["options"], key=f"q_{q_idx}")
        if len(st.session_state.selected_answers) <= q_idx:
            st.session_state.selected_answers.append(choice)
        else:
            st.session_state.selected_answers[q_idx] = choice

        # Real-time score & progress
        correct_so_far = sum(
            1 for i, q in enumerate(st.session_state.questions[:q_idx+1])
            if i < len(st.session_state.selected_answers) and q["a"] == st.session_state.selected_answers[i]
        )
        progress_percent = int(((q_idx+1) / len(st.session_state.questions)) * 100)
        st.progress(progress_percent)
        st.info(f"✅ Score so far: {correct_so_far}/{q_idx+1}")

        # Columns for navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Previous", disabled=(q_idx == 0)):
                st.session_state.current_question -= 1
                st.rerun()
        with col2:
            if st.button("Next ➡️"):
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(st.session_state.questions):
                    # Calculate final score
                    correct = sum(
                        1 for i, q in enumerate(st.session_state.questions)
                        if q["a"] == st.session_state.selected_answers[i]
                    )
                    st.session_state.score = correct
                    st.session_state.results.append({
                        "section": "Practice",
                        "difficulty": difficulty,
                        "score": correct,
                        "total": len(st.session_state.questions),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.session_state.in_test = False

                    # Confetti for high score
                    score_percentage = correct/len(st.session_state.questions)
                    if score_percentage >= 0.8:
                        rain(emoji="🎉", font_size=40, falling_speed=5, animation_length=3)

                    # Badge System
                    if score_percentage >= 0.8:
                        st.markdown("<div class='badge gold'>🥇 Gold Badge</div>", unsafe_allow_html=True)
                    elif score_percentage >= 0.5:
                        st.markdown("<div class='badge silver'>🥈 Silver Badge</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='badge bronze'>🥉 Bronze Badge</div>", unsafe_allow_html=True)

                    # Animated Circular Score Gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=correct,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Test Score", 'font': {'size': 24}},
                        delta={'reference': len(st.session_state.questions), 'increasing': {'color': "green"}},
                        gauge={
                            'axis': {'range': [0, len(st.session_state.questions)]},
                            'bar': {'color': "rgba(0,85,165,0.8)"},
                            'steps': [
                                {'range': [0, len(st.session_state.questions)*0.5], 'color': "red"},
                                {'range': [len(st.session_state.questions)*0.5, len(st.session_state.questions)*0.8], 'color': "yellow"},
                                {'range': [len(st.session_state.questions)*0.8, len(st.session_state.questions)], 'color': "green"}
                            ],
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                    st.success(f"🎉 Test Completed! Your Score: {correct}/{len(st.session_state.questions)}")
                st.rerun()

# -------------------------------
# Other Sections
# -------------------------------
elif section == "Mock Interview":
    st.subheader("🎤 Mock Interview")
    st.info("Simulate a real interview environment. (Coming Soon!)")

elif section == "MCQ Quiz":
    st.subheader("🧠 MCQ Quiz")
    st.info("Timed quizzes to test your knowledge. (Coming Soon!)")

elif section == "Pseudocode":
    st.subheader("💡 Pseudocode Practice")
    st.info("Improve your logic-building skills. (Coming Soon!)")

elif section == "Results":
    st.subheader("📊 Results")
    if len(st.session_state.results) == 0:
        st.info("No results yet. Complete a test to see your results.")
    else:
        for rec in st.session_state.results:
            section_name = rec.get("section", "Unknown")
            diff = rec.get("difficulty", "N/A")
            score = rec.get("score", 0)
            total = rec.get("total", 0)
            timestamp = rec.get("timestamp", "")
            color = "green" if score/total >= 0.8 else "yellow" if score/total >=0.5 else "red"
            st.markdown(f"<div style='padding:10px; border-radius:10px; background:{color};'>"
                        f"**{section_name}** — {diff} | Score: **{score}/{total}** | ⏱️ {timestamp}</div>", unsafe_allow_html=True)

elif section == "Analytics":
    st.subheader("📈 Performance Analytics")
    if len(st.session_state.results) == 0:
        st.info("No data available for analytics.")
    else:
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df.style.background_gradient(cmap='Blues'))

elif section == "History":
    st.subheader("🕓 History")
    if len(st.session_state.results) == 0:
        st.info("No past history found.")
    else:
        df = pd.DataFrame(st.session_state.results)
        st.table(df)
