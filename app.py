# app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Interview Preparation Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
            padding: 20px;
        }
        .stTabs [role="tablist"] {
            justify-content: center;
        }
        .stTabs [role="tab"] {
            padding: 10px 25px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 10px;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #2e7d32;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("📚 Navigation")
main_section = st.sidebar.radio(
    "Go to:",
    ["Practice", "Mock Interview", "MCQ Quiz", "Pseudocode", "Results", "Performance & Analytics", "History"]
)

# -------------------------------
# PRACTICE SECTION
# -------------------------------
if main_section == "Practice":
    st.title("🧠 Practice Section")
    tab1, tab2, tab3, tab4 = st.tabs(["Data Structures", "Algorithms", "Python", "Aptitude"])

    with tab1:
        st.subheader("📘 Data Structures Practice")
        st.write("Work on common problems like arrays, linked lists, stacks, and queues.")

    with tab2:
        st.subheader("📗 Algorithms Practice")
        st.write("Solve sorting, searching, and optimization algorithm challenges.")

    with tab3:
        st.subheader("🐍 Python Practice")
        st.write("Sharpen your Python fundamentals and syntax through hands-on exercises.")

    with tab4:
        st.subheader("🧮 Aptitude Practice")
        st.write("Test your mathematical and logical reasoning skills.")

# -------------------------------
# MOCK INTERVIEW SECTION
# -------------------------------
elif main_section == "Mock Interview":
    st.title("🎤 Mock Interview Section")
    tab1, tab2 = st.tabs(["HR Round", "Technical Round"])

    with tab1:
        st.subheader("💬 HR Interview Simulation")
        st.write("Practice common HR questions to boost your confidence.")

    with tab2:
        st.subheader("🖥 Technical Interview Simulation")
        st.write("Get technical questions from different domains to test your preparation.")

# -------------------------------
# MCQ QUIZ SECTION
# -------------------------------
elif main_section == "MCQ Quiz":
    st.title("🧩 MCQ Quiz Section")
    tab1, tab2, tab3 = st.tabs(["Easy", "Medium", "Hard"])

    with tab1:
        st.subheader("🟢 Easy Quiz")
        st.write("Start with basic level questions to warm up.")

    with tab2:
        st.subheader("🟠 Medium Quiz")
        st.write("Try intermediate-level challenges to test your skills.")

    with tab3:
        st.subheader("🔴 Hard Quiz")
        st.write("Attempt advanced and tricky questions for experts.")

# -------------------------------
# PSEUDOCODE SECTION
# -------------------------------
elif main_section == "Pseudocode":
    st.title("📜 Pseudocode Section")
    tab1, tab2, tab3 = st.tabs(["Logical Flow", "Output Prediction", "Code Completion"])

    with tab1:
        st.subheader("🧠 Logical Flow Problems")
        st.write("Understand the control flow and structure of code logic.")

    with tab2:
        st.subheader("🔍 Output Prediction")
        st.write("Guess the output of given code snippets to improve logical reasoning.")

    with tab3:
        st.subheader("💻 Code Completion")
        st.write("Complete missing parts of code to make it functional.")

# -------------------------------
# RESULTS SECTION
# -------------------------------
elif main_section == "Results":
    st.title("📈 Results")
    tab1, tab2 = st.tabs(["Latest Result", "Overall Stats"])

    with tab1:
        st.subheader("🏁 Latest Test Result")
        st.write("Your most recent test performance details will appear here.")

    with tab2:
        st.subheader("📊 Overall Performance Statistics")
        st.write("Summary of your scores and progress over time.")

# -------------------------------
# PERFORMANCE & ANALYTICS SECTION
# -------------------------------
elif main_section == "Performance & Analytics":
    st.title("📊 Performance & Analytics")
    tab1, tab2, tab3 = st.tabs(["Accuracy Graph", "Time Taken", "Topic Analysis"])

    with tab1:
        st.subheader("📈 Accuracy Over Time")
        st.line_chart(pd.DataFrame(np.random.randn(10, 2), columns=["Accuracy", "Attempts"]))

    with tab2:
        st.subheader("⏱ Average Time Per Question")
        st.bar_chart(pd.DataFrame(np.random.randint(10, 100, size=(5, 2)), columns=["Easy", "Hard"]))

    with tab3:
        st.subheader("📚 Topic-Wise Analysis")
        st.write("Analyze your performance across different categories and difficulty levels.")

# -------------------------------
# HISTORY SECTION
# -------------------------------
elif main_section == "History":
    st.title("🕓 Test History")
    tab1, tab2 = st.tabs(["Previous Tests", "Score Summary"])

    with tab1:
        st.subheader("📘 Previous Test Records")
        st.table(pd.DataFrame({
            "Date": ["2025-10-01", "2025-10-10", "2025-10-20"],
            "Section": ["MCQ Quiz", "Practice", "Mock Interview"],
            "Score": [78, 85, 92]
        }))

    with tab2:
        st.subheader("📄 Score Summary")
        st.write("Overview of all past performance records for better tracking.")
