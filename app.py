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
question_bank = {
    "Practice": {
        "Easy": [
            {"q": "If 5x + 3 = 18, what is x?", "a": "3", "options": ["2","3","4","5"]},
            {"q": "What is 15% of 200?", "a": "30", "options": ["20","25","30","35"]},
            {"q": "Which of these is a futuristic AI technology?", "a": "Quantum AI", "options": ["Quantum AI","Classic AI","Manual Automation","Typewriter"]},
            {"q": "Next in series: 2, 4, 8, 16, ?", "a": "32", "options": ["24","30","32","36"]}
        ],
        "Medium": [
            {"q": "A man can do a job in 10 days, work done in 5 days?", "a": "50%", "options": ["40%","50%","60%","70%"]},
            {"q": "Probability of picking red ball from bag with 5R,3B,2G?", "a": "1/2", "options": ["1/3","1/2","1/5","2/5"]},
            {"q": "Which futuristic technology can learn from experience?", "a": "Machine Learning", "options": ["Steam Engine","Machine Learning","Typewriter","Analog Computer"]}
        ],
        "Hard": [
            {"q": "Solve: 3(x-2) + 4 = 19", "a": "5", "options": ["4","5","6","7"]},
            {"q": "5 men do work in 20 days, 10 men do in?", "a": "10 days", "options": ["8 days","10 days","12 days","15 days"]},
            {"q": "Which technology uses qubits for computation?", "a": "Quantum Computing", "options": ["Classical Computing","Quantum Computing","Blockchain","Neural Networks"]}
        ]
    },
    "Mock Interview": {
        "Easy": [
            {"q": "What is Python?", "a": "Programming Language", "options":["Snake","Programming Language","Game","OS"]},
            {"q": "What is your greatest strength?", "a": "Adaptability", "options":["Adaptability","Patience","Confidence","Skill"]},
            {"q": "Name a futuristic programming paradigm?", "a": "Quantum programming", "options":["Procedural","Quantum programming","OOP","Functional"]}
        ],
        "Medium": [
            {"q": "Explain inheritance in OOP", "a": "Child inherits parent properties", "options":["Parent inherits child","Child inherits parent properties","No inheritance","Multiple inheritance only"]},
            {"q": "Describe a challenging situation and resolution", "a": "Explain experience", "options":["Avoided","Explained experience","Ignored","Delegated"]},
            {"q": "Which AI concept predicts future events?", "a": "Predictive Analytics", "options":["Reactive AI","Predictive Analytics","Rule-based AI","Quantum AI"]}
        ],
        "Hard": [
            {"q": "Explain multithreading vs multiprocessing", "a": "Threads share memory; processes don't", "options":["Threads separate memory","Threads share memory; processes don't","Processes share memory","Both same"]},
            {"q": "Which futuristic AI can generate human-like text?", "a": "Generative AI", "options":["Classical AI","Generative AI","Reactive AI","Narrow AI"]}
        ]
    },
    "MCQ Quiz": {
        "Easy": [
            {"q": "Which language is used for AI?", "a": "Python", "options":["Python","C","Java","HTML"]},
            {"q": "CSS is used for?", "a": "Styling web pages", "options":["Functionality","Database","Styling web pages","Backend"]},
            {"q": "Which futuristic technology mimics the human brain?", "a": "Neural Networks", "options":["Robotics","Neural Networks","IoT","Blockchain"]}
        ],
        "Medium": [
            {"q": "What does len() do in Python?", "a": "Returns length", "options":["Returns max","Returns length","Returns value","None"]},
            {"q": "Python multiple inheritance supported?", "a": "Yes", "options":["No","Yes","Partially","Depends"]},
            {"q": "Which AI can create images from text?", "a": "Generative AI", "options":["Reinforcement AI","Generative AI","Reactive AI","Narrow AI"]}
        ],
        "Hard": [
            {"q": "Explain Python metaclass", "a": "Class of a class", "options":["Instance","Class of a class","Function","Loop"]},
            {"q": "Difference between classmethod and staticmethod?", "a": "Classmethod takes cls, staticmethod takes none", "options":["Both take self","Both take cls","Classmethod takes cls, staticmethod takes none","None"]},
            {"q": "Which futuristic tech uses qubits?", "a": "Quantum Computing", "options":["Classical Computing","Quantum Computing","AI","Blockchain"]}
        ]
    },
    "Pseudocode": {
        "Easy": [
            {"q": "Write pseudocode to find max of two numbers", "a": "If a>b then max=a else max=b", "options":["max=a+b","If a>b then max=a else max=b","max=a*b","None"]},
            {"q": "Check if number is even", "a": "If n mod 2 = 0 then even else odd", "options":["If n%2=0 then even else odd","n%2==1 then odd","Check n/2","None"]}
        ],
        "Medium": [
            {"q": "Sort array using bubble sort", "a": "For i=1 to n For j=1 to n-i if a[j]>a[j+1] swap", "options":["Bubble sort logic","For i=1 to n For j=1 to n-i if a[j]>a[j+1] swap","Sort manually","None"]},
            {"q": "Find GCD of two numbers", "a": "While b!=0 t=b b=a%b a=t return a", "options":["Euclid","While b!=0 t=b b=a%b a=t return a","Loop subtract","None"]}
        ],
        "Hard": [
            {"q": "Implement merge sort", "a": "Divide, merge recursively", "options":["Divide, merge recursively","Quick sort","Bubble sort","None"]},
            {"q": "Find shortest path in graph", "a": "Dijkstra or BFS", "options":["DFS","Dijkstra or BFS","Greedy","None"]}
        ]
    }
}

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


