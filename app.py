# app.py
import streamlit as st
import random, time
from streamlit_extras.let_it_rain import rain

# ------------------ CSS ------------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #e0f7fa, #f1f8e9); font-family: 'Segoe UI', sans-serif; }
.header-title { text-align:center; font-size:2.5em; font-weight:bold; color:#00796b; margin-bottom:5px;}
.header-tagline { text-align:center; font-size:1.3em; color:#004d40; margin-bottom:25px;}
.description { text-align:center; font-size:1.1em; color:#00695c; margin-bottom:40px;}
.stButton>button { background-color:#00796b; color:white; border-radius:12px; padding:0.5em 2em; font-weight:bold; transition: all 0.3s ease;}
.stButton>button:hover { background-color:#004d40; transform:scale(1.05);}
.question-card { padding:25px; border-radius:20px; background: rgba(0,121,107,0.1); margin-bottom:20px; transition:all 0.3s ease;}
.nav-buttons { display:flex; justify-content:space-between; margin-top:20px;}
.timer { text-align:center; font-size:1.2em; font-weight:bold; color:#004d40; margin-bottom:15px;}
.progress-bar { height:20px; border-radius:10px; background:#B2DFDB; margin-bottom:20px;}
.progress-bar-fill { height:100%; border-radius:10px; background:#00796b; transition: width 0.5s;}
.badge { display:inline-block; padding:5px 15px; margin:5px; border-radius:15px; background:#FFD700; color:#004d40; font-weight:bold; transition:all 0.3s ease; }
.footer { text-align:center; font-size:14px; color:#555; margin-top:40px; padding:10px;}
</style>
""", unsafe_allow_html=True)

# ------------------ Session State ------------------
if "in_test" not in st.session_state: st.session_state.in_test = False
if "current_question" not in st.session_state: st.session_state.current_question = 0
if "selected_answers" not in st.session_state: st.session_state.selected_answers = []
if "shuffled_questions" not in st.session_state: st.session_state.shuffled_questions = []
if "start_time" not in st.session_state: st.session_state.start_time = None
if "duration" not in st.session_state: st.session_state.duration = 300
if "badges" not in st.session_state: st.session_state.badges = []
if "consecutive_correct" not in st.session_state: st.session_state.consecutive_correct = 0

# ------------------ Question Bank ------------------
QUESTION_BANK = {
    "Practice": {"Easy":[
        {"q":"If 5x + 3 = 18, what is x?","a":"3","options":["2","3","4","5"]},
        {"q":"If a:b = 2:3 and b:c = 4:5, find a:c","a":"8:15","options":["2:5","8:15","4:5","6:7"]},
        {"q":"Sum of angles in a triangle?","a":"180","options":["90","180","360","270"]},
    ]},
    "Mock Interview": {"Easy":[
        {"q":"What is Python?","a":"Programming Language","options":["Snake","Programming Language","Game","OS"]},
    ]}
}

# ------------------ Landing Page ------------------
if not st.session_state.in_test:
    st.markdown('<div class="header-title">🚀 Interview Preparation Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-tagline">Sharpen your skills, ace your interviews!</div>', unsafe_allow_html=True)
    st.markdown('<div class="description">Select a section & difficulty, then start practicing!</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    with col1: section = st.selectbox("Select Section", list(QUESTION_BANK.keys()))
    with col2: difficulty = st.selectbox("Select Difficulty", ["Easy","Medium","Hard"])

    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("Start Test"):
        st.session_state.in_test = True
        st.session_state.current_question = 0
        st.session_state.selected_answers = []
        st.session_state.start_time = time.time()
        questions = QUESTION_BANK.get(section, {}).get(difficulty, [])[:]
        random.shuffle(questions)
        st.session_state.shuffled_questions = questions
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ Test Page ------------------
if st.session_state.in_test:
    questions = st.session_state.shuffled_questions
    q_idx = st.session_state.current_question
    q_data = questions[q_idx]

    # Timer & Progress Bar
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, st.session_state.duration - elapsed)
    minutes, seconds = divmod(remaining, 60)
    percent = (remaining/st.session_state.duration)*100

    st.markdown(f"<div class='timer'>⏰ Time Remaining: {minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='progress-bar'><div class='progress-bar-fill' style='width:{percent}%'></div></div>", unsafe_allow_html=True)

    # Question Card
    st.markdown(f"<div class='question-card'><b>Q{q_idx+1}:</b> {q_data['q']}</div>", unsafe_allow_html=True)
    answer = st.radio("Select your answer", q_data['options'], key=q_idx)

    # Navigation Buttons
    col_prev, col_save, col_next = st.columns([1,1,1])
    with col_prev:
        if q_idx>0 and st.button("Previous Question"): st.session_state.current_question-=1
    with col_save:
        if st.button("Save Answer"):
            if len(st.session_state.selected_answers)>q_idx: st.session_state.selected_answers[q_idx]=answer
            else: st.session_state.selected_answers.append(answer)
    with col_next:
        if st.button("Next Question"):
            if len(st.session_state.selected_answers)<=q_idx: st.session_state.selected_answers.append(answer)
            if q_idx+1<len(questions): st.session_state.current_question+=1

    # Submit Test
    if st.button("Submit Test"):
        st.session_state.in_test=False
        score = sum(1 for i, ans in enumerate(st.session_state.selected_answers) if ans==questions[i]['a'])
        st.success(f"🎉 Test Completed! Your score: {score}/{len(questions)}")

        # Badge: Perfect Score
        if score==len(questions) and "🏆 Perfect Score" not in st.session_state.badges:
            st.session_state.badges.append("🏆 Perfect Score")
            st.markdown('<div class="badge">🏆 Perfect Score</div>', unsafe_allow_html=True)
            rain()

        # Badge: Section Completed
        badge_name = f"✅ Completed {section}"
        if badge_name not in st.session_state.badges:
            st.session_state.badges.append(badge_name)
            st.markdown(f'<div class="badge">{badge_name}</div>', unsafe_allow_html=True)

        # Badge: Consecutive Correct (check streaks)
        streak = 0
        for i, ans in enumerate(st.session_state.selected_answers):
            if ans == questions[i]['a']:
                streak += 1
            else:
                streak = 0
            if streak >=3 and "🔥 3 Correct Streak" not in st.session_state.badges:
                st.session_state.badges.append("🔥 3 Correct Streak")
                st.markdown('<div class="badge">🔥 3 Correct Streak</div>', unsafe_allow_html=True)

    # Display All Badges
    st.markdown("<div style='margin-top:20px;'><b>Badges Earned:</b></div>", unsafe_allow_html=True)
    for badge in st.session_state.badges:
        st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)

# ------------------ Footer ------------------
st.markdown('<div class="footer">Developed by Anil & Team</div>', unsafe_allow_html=True)
