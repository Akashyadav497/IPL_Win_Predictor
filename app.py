import streamlit as st
import pickle
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2rem;
        color: #1E3A8A;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    .metric-val {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1E293B;
    }
    .metric-lbl {
        font-size: 0.8rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #2563EB , #10B981);
    }
</style>
""", unsafe_allow_html=True)

# IPL teams list
teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

# Host cities list
cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
]

# Sidebar
with st.sidebar:
    st.header("ℹ️ About the App")
    st.markdown("""
    This **IPL Win Predictor** estimates the real-time winning probability of chasing teams in IPL second-innings matches using Machine Learning.

    **How to use:**
    1. Select batting & bowling teams.
    2. Pick the match venue / host city.
    3. Enter target score & current match state.
    4. Click **Predict Win Probability**.
    """)
    st.divider()
    st.caption("Powered by Scikit-Learn & Streamlit")

# Main Header
st.markdown("<h1 class='main-title'>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Machine Learning-based live 2nd innings win probability estimator</p>", unsafe_allow_html=True)

# Load model safely
model_path = os.path.join(os.path.dirname(__file__), 'pipe.pkl') if '__file__' in locals() else 'pipe.pkl'
pipe = None
try:
    with open(model_path, 'rb') as f:
        pipe = pickle.load(f)
except Exception as e:
    st.error(f"Error loading trained model (`pipe.pkl`): {e}")

# Team Selection
st.subheader("1. Team & Venue Details")
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Batting Team (Chasing)', sorted(teams), index=teams.index('Mumbai Indians') if 'Mumbai Indians' in teams else 0)
with col2:
    bowling_team_options = [team for team in sorted(teams) if team != batting_team]
    bowling_team = st.selectbox('Bowling Team (Defending)', bowling_team_options, index=0)

# City Selection
selected_city = st.selectbox('Host City / Venue', sorted(cities), index=sorted(cities).index('Mumbai') if 'Mumbai' in sorted(cities) else 0)

st.divider()

# Match Situation
st.subheader("2. Current Match Situation")

col_target, col_score = st.columns(2)
with col_target:
    target = st.number_input('Target Score', min_value=1, max_value=350, value=180, step=1, help="Total runs scored by the 1st innings team + 1")
with col_score:
    score = st.number_input('Current Score', min_value=0, max_value=350, value=95, step=1, help="Current runs scored by the batting team")

col_overs, col_wkts = st.columns(2)
with col_overs:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, value=10.0, step=0.1, format="%.1f", help="Overs bowled (e.g., 10.2)")
with col_wkts:
    wickets_out = st.number_input('Wickets Lost', min_value=0, max_value=10, value=2, step=1, help="Number of wickets fallen so far (0-10)")

# Calculate match dynamics
overs_completed_int = int(overs)
balls_in_over = int(round((overs - overs_completed_int) * 10))

# Validate overs ball count (e.g. 10.6 is invalid in cricket)
invalid_balls = balls_in_over >= 6
total_balls_bowled = (overs_completed_int * 6) + balls_in_over
balls_left = 120 - total_balls_bowled
runs_left = target - score
wickets_in_hand = 10 - wickets_out
crr = score / overs if overs > 0 else 0.0
rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0.0

# Display Live Match Metrics
st.markdown("##### Match Snapshot")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Runs Needed</div><div class='metric-val'>{max(0, runs_left)}</div></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Balls Left</div><div class='metric-val'>{max(0, balls_left)}</div></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Current RR</div><div class='metric-val'>{crr:.2f}</div></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Required RR</div><div class='metric-val'>{rrr:.2f}</div></div>", unsafe_allow_html=True)

st.write("")

# Predict Button
predict_btn = st.button('🎯 Predict Probability', use_container_width=True, type="primary")

if predict_btn:
    # Input Validations
    if batting_team == bowling_team:
        st.error("⚠️ Batting and Bowling teams cannot be the same. Please choose distinct teams.")
    elif invalid_balls:
        st.warning(f"⚠️ Invalid overs value ({overs:.1f}). Over decimal represents legal balls (0.1 to 0.5). For example, 10.6 is 11.0 overs.")
    elif total_balls_bowled > 120:
        st.warning("⚠️ Overs completed cannot exceed 20.0 overs (120 balls).")
    elif score >= target:
        st.success(f"🎉 **{batting_team}** has already reached the target and won the match!")
    elif wickets_out >= 10:
        st.error(f"❌ **{batting_team}** is all out! **{bowling_team}** wins the match.")
    elif balls_left <= 0:
        st.error(f"⏰ All 20 overs have been bowled. **{batting_team}** fell short by {runs_left} runs! **{bowling_team}** wins.")
    elif pipe is None:
        st.error("Trained model pipeline is not loaded. Please ensure `pipe.pkl` exists in the application directory.")
    else:
        # Prepare feature DataFrame matching model requirements
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_in_hand],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        try:
            result = pipe.predict_proba(input_df)
            loss_prob = result[0][0]
            win_prob = result[0][1]

            win_pct = round(win_prob * 100)
            loss_pct = round(loss_prob * 100)

            # Ensure total adds to 100% cleanly
            if win_pct + loss_pct != 100:
                loss_pct = 100 - win_pct

            st.markdown("### 📊 Prediction Result")

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(
                    label=f"🏏 {batting_team} (Chasing)",
                    value=f"{win_pct}%",
                    delta="Win Probability"
                )
            with res_col2:
                st.metric(
                    label=f"🎯 {bowling_team} (Defending)",
                    value=f"{loss_pct}%",
                    delta="Win Probability"
                )

            st.markdown(f"**Win Probability Distribution**")
            st.progress(win_pct / 100.0)

            if win_pct > loss_pct:
                st.success(f"🔥 **{batting_team}** has an upper hand with a **{win_pct}%** chance to chase down {target} runs.")
            elif win_pct < loss_pct:
                st.info(f"🛡️ **{bowling_team}** is in control, defending {target} runs with a **{loss_pct}%** win probability.")
            else:
                st.warning("⚖️ The match is in dead heat balance! Both teams have an equal 50% chance of winning.")

        except Exception as err:
            st.error(f"Prediction failed due to an unexpected error: {err}")
