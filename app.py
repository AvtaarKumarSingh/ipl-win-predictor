import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏆",
    layout="wide"
)

pipe = pickle.load(open("pipe.pkl", "rb"))

# ---------------- CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #000000, #8B0000);
        color: white;
    }

    h1, h2, h3, p, label {
        color: white !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    .result-box {
        background: rgba(0,0,0,0.6);
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
    }

    .stButton>button {
        background-color: #8B0000;
        color: white;
        border-radius: 10px;
        height: 45px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align:center;'>🏆 IPL Win Predictor</h1>",
    unsafe_allow_html=True
)

teams = [
    'Sunrisers Hyderabad','Mumbai Indians','Royal Challengers Bangalore',
    'Kolkata Knight Riders','Kings XI Punjab','Chennai Super Kings',
    'Rajasthan Royals','Delhi Capitals'
]

cities = [
    'Hyderabad','Bangalore','Mumbai','Indore','Kolkata','Delhi',
    'Chandigarh','Jaipur','Chennai','Cape Town','Port Elizabeth',
    'Durban','Centurion','East London','Johannesburg','Ahmedabad',
    'Cuttack','Nagpur','Dharamsala','Visakhapatnam','Pune','Ranchi',
    'Abu Dhabi','Sharjah','Mohali','Bengaluru'
]

col1, col2, col3 = st.columns(3)

with col1:
    batting_team = st.selectbox("Batting Team", sorted(teams))

with col2:
    bowling_team = st.selectbox("Bowling Team", sorted(teams))

with col3:
    selected_city = st.selectbox("City", sorted(cities))

target = st.number_input("Target Score", min_value=1)

col4, col5, col6 = st.columns(3)

with col4:
    score = st.number_input("Current Score", min_value=0)

with col5:
    overs = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, step=0.1)

with col6:
    wickets_out = st.number_input("Wickets Out", min_value=0, max_value=10)

if batting_team == bowling_team:
    st.error("Batting and Bowling teams cannot be the same.")
    st.stop()
if st.button("🚀 Predict Probability"):

    if score >= target:
        st.success(f"🎉 {batting_team} WON THE MATCH!")
        st.balloons()

    elif wickets_out >= 10:
        st.error(f"❌ {batting_team} LOST THE MATCH!")
        st.success(f"🏆 {bowling_team} WON THE MATCH!")

    elif overs >= 20:
        st.error(f"❌ {batting_team} LOST THE MATCH!")
        st.success(f"🏆 {bowling_team} WON THE MATCH!")

    elif overs <= 0:
        st.warning("Please enter at least 0.1 overs completed.")

    else:
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_remaining = 10 - wickets_out

        crr = score / overs
        rrr = (runs_left * 6) / balls_left

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_remaining],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)

        loss = result[0][0]
        win = result[0][1]

        st.markdown("## 🏏 Match Prediction Result")

        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.progress(int(win * 100))

        colA, colB = st.columns(2)

        with colA:
            st.success(f"{batting_team}\nWin Chance: {win*100:.2f}%")

        with colB:
            st.error(f"{bowling_team}\nWin Chance: {loss*100:.2f}%")

        st.markdown('</div>', unsafe_allow_html=True)

        if win >= 0.80:
            st.balloons()