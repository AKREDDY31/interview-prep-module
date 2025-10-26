import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# ⚙️ App Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI Interview Preparation Platform",
    layout="wide",
    page_icon="🧠",
)

# --------------------------------------------------
# 🌈 Custom Styling for a Modern Look
# --------------------------------------------------
st.markdown("""
    <style>
    body {background-color: #f5f7fa;}
    .main {padding: 1rem 2rem;}
    h1, h2, h3 {color: #2b6777 !important;}
    .stTabs [role="tablist"] {justify-content: center;}
    .stTabs [role="tab"] {
        font-size: 17px !important;
        font-weight: 600;
        color: #2b6777;
        padding: 10px 24px;
        border-radius: 10px;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #2b6777;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 🧭 Sidebar Navigation
# --------------------------------------------------
st.sidebar.title("📚 Navigation")
menu = st.sidebar.radio(
    "Choose Section",
    ["Practice", "Mock Interview", "MCQ Quiz", "Pseudocode", "Results", "Performance & Analytics", "History"]
)

# --------------------------------------------------
# 🧠 PRACTICE
# --------------------------------------------------
if menu == "Practice":
    st.title("🧠 Practice")
    tabs = st.tabs(["Data Structures", "Algorithms", "Python", "Aptitude"])

    with tabs[0]:
        st.subheader("📘 Data Structures")
        st.info("Practice problems on Arrays, Linked Lists, Stacks, Queues, Trees, and Graphs.")

    with tabs[1]:
        st.subheader("📗 Algorithms")
        st.info("Work on Sorting, Searching, Dynamic Programming, and Greedy problems.")

    with tabs[2]:
        st.subheader("🐍 Python")
        st.info("Strengthen Python concepts — functions, loops, OOP, and error handling.")

    with tabs[3]:
        st.subheader("🧮 Aptitude")
        st.info("Sharpen your logical and mathematical reasoning skills.")


# --------------------------------------------------
# 🎤 MOCK INTERVIEW
# --------------------------------------------------
elif menu == "Mock Interview":
    st.title("🎤 Mock Interview")
    tabs = st.tabs(["HR Round", "Technical Round"])

    with tabs[0]:
        st.subheader("💬 HR Round")
        st.success("Simulate HR interview questions to improve your communication skills.")

    with tabs[1]:
        st.subheader("🖥 Technical Round")
        st.success("Answer real-world technical questions to simulate an interview environment.")


# --------------------------------------------------
# 🧩 MCQ QUIZ
# --------------------------------------------------
elif menu == "MCQ Quiz":
    st.title("🧩 MCQ Quiz")
    tabs = st.tabs(["Easy", "Medium", "Hard"])

    for level, emoji in zip(["Easy", "Medium", "Hard"], ["🟢", "🟠", "🔴"]):
        with tabs[["Easy", "Medium", "Hard"].index(level)]:
            st.subheader(f"{emoji} {level} Level")
            st.info(f"Take a {level.lower()} level MCQ quiz to assess your understanding.")


# --------------------------------------------------
# 📜 PSEUDOCODE
# --------------------------------------------------
elif menu == "Pseudocode":
    st.title("📜 Pseudocode")
    tabs = st.tabs(["Logical Flow", "Output Prediction", "Code Completion"])

    with tabs[0]:
        st.subheader("🧠 Logical Flow")
        st.info("Understand how control structures and loops form the logical flow.")

    with tabs[1]:
        st.subheader("🔍 Output Prediction")
        st.info("Predict the outputs of given code snippets to test understanding.")

    with tabs[2]:
        st.subheader("💻 Code Completion")
        st.info("Fill in missing parts of pseudocode to make it functional.")


# --------------------------------------------------
# 📈 RESULTS
# --------------------------------------------------
elif menu == "Results":
    st.title("📈 Results")
    tabs = st.tabs(["Latest Result", "Overall Stats"])

    with tabs[0]:
        st.subheader("🏁 Latest Test Result")
        st.metric("Latest Score", "89%", "↑ 4% since last test")

    with tabs[1]:
        st.subheader("📊 Overall Stats")
        st.bar_chart(pd.DataFrame({
            "Section": ["Practice", "MCQ", "Mock", "Pseudocode"],
            "Score": [85, 90, 78, 88]
        }).set_index("Section"))


# --------------------------------------------------
# 📉 PERFORMANCE & ANALYTICS
# --------------------------------------------------
elif menu == "Performance & Analytics":
    st.title("📉 Performance & Analytics")
    tabs = st.tabs(["Accuracy Graph", "Time Taken", "Topic Analysis"])

    with tabs[0]:
        st.subheader("📈 Accuracy Over Time")
        st.line_chart(pd.DataFrame(np.random.randint(70, 100, (10, 1)), columns=["Accuracy"]))

    with tabs[1]:
        st.subheader("⏱ Time Taken per Question")
        st.bar_chart(pd.DataFrame(np.random.randint(5, 30, (5, 1)), columns=["Seconds"]))

    with tabs[2]:
        st.subheader("📚 Topic Analysis")
        st.dataframe(pd.DataFrame({
            "Topic": ["Python", "DS", "Algo", "Aptitude"],
            "Correct": [45, 38, 50, 40],
            "Total": [50, 45, 60, 50]
        }))


# --------------------------------------------------
# 🕓 HISTORY
# --------------------------------------------------
elif menu == "History":
    st.title("🕓 History")
    tabs = st.tabs(["Previous Tests", "Score Summary"])

    with tabs[0]:
        st.subheader("📘 Previous Tests")
        st.table(pd.DataFrame({
            "Date": ["2025-10-10", "2025-10-15", "2025-10-22"],
            "Section": ["Practice", "Mock Interview", "MCQ Quiz"],
            "Score (%)": [85, 78, 92]
        }))

    with tabs[1]:
        st.subheader("📄 Summary")
        st.metric("Average Score", "85%", "↑ 3% Overall Improvement")
