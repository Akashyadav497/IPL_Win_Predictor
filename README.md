# 🏏 IPL Win Predictor

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive Machine Learning web application designed to predict the real-time winning probability of chasing teams during the 2nd innings of Indian Premier League (IPL) matches.

---

## 📌 Project Overview

In T20 cricket, particularly in the IPL, match momentum swings rapidly within a span of a few deliveries. The **IPL Win Predictor** models the dynamic state of a chase by taking real-time match parameters — required runs, balls remaining, wickets down, current run rate (CRR), and required run rate (RRR) — to evaluate the likelihood of victory for both the batting and bowling sides.

---

## ✨ Key Features

- **Intuitive & Responsive UI:** Clean Streamlit interface styled with custom visual enhancements.
- **Smart Team & Venue Selectors:** Dynamic dropdown filters preventing selecting identical teams for batting and bowling.
- **Live Match Snapshot Metrics:** Instant computation of **Runs Needed**, **Balls Left**, **Current Run Rate (CRR)**, and **Required Run Rate (RRR)**.
- **Accurate Probability Display:** Dual-team win percentage display alongside an intuitive visual probability progress bar.
- **Robust Input Validation & Edge Case Handling:**
  - Automatic detection when the target has already been reached.
  - Graceful handling when all 10 wickets are down (All Out).
  - Detection of completed 20 overs (120 balls).
  - Validation of cricket over ball decimals (e.g., flags 10.6+ as invalid ball count).
- **Lightweight Architecture:** Fast inference using a Scikit-Learn `Pipeline` (`OneHotEncoder` + `LogisticRegression`).

---

## ⚙️ How the Prediction System Works

1. **User Inputs Match State:**
   - Batting & Bowling teams.
   - Host city / venue.
   - Target score, current score, overs completed, and wickets lost.
2. **Feature Engineering:**
   - $\text{Runs Left} = \text{Target} - \text{Score}$
   - $\text{Balls Left} = 120 - (\text{Overs} \times 6)$
   - $\text{Wickets in Hand} = 10 - \text{Wickets Lost}$
   - $\text{Current Run Rate (CRR)} = \frac{\text{Score}}{\text{Overs}}$
   - $\text{Required Run Rate (RRR)} = \frac{\text{Runs Left} \times 6}{\text{Balls Left}}$
3. **Pipeline Inference:**
   - Categorical features (`batting_team`, `bowling_team`, `city`) are transformed via `OneHotEncoder`.
   - Numerical features pass through to a calibrated classifier (`LogisticRegression`).
   - The model computes normalized probabilities: $P(\text{Win})$ and $P(\text{Loss})$.

---

## 📊 Dataset Information

The predictive model is built on historical IPL ball-by-ball and match dataset records (2008–present), capturing:
- Match details (match ID, city, teams, toss decisions).
- Second innings ball-by-ball progressions (runs scored, wickets fallen, extras).
- Match outcomes (winner team).

---

## 🗂️ Project Folder Structure

```text
IPL_Win_Predictor/
│
├── app.py              # Main Streamlit web application
├── pipe.pkl            # Pre-trained ML Pipeline (Preprocessing + Model)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation and setup guide
```

---

## 💻 Technologies Used

- **Language:** Python
- **Web Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Machine Learning:** [Scikit-Learn](https://scikit-learn.org/)
- **Model Serialization:** Pickle

---

## 🚀 Installation Instructions

### Prerequisites
Make sure you have Python 3.9 or higher installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/IPL_Win_Predictor.git
   cd IPL_Win_Predictor
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃‍♂️ How to Run the Project

Launch the Streamlit app with the following command:

```bash
streamlit run app.py
```

Once executed, your browser will open the app automatically at `http://localhost:8501`.

---

## 📷 Screenshots

| Match Input & Live Situation | Prediction Results & Win Distribution |
| :---: | :---: |
| *(Placeholder: Add screenshot of match inputs)* | *(Placeholder: Add screenshot of prediction cards)* |

> *Tip: Place your screenshots in an `assets/` folder and link them here.*

---

## 🔮 Future Improvements

- Add player-level analytics (impact of batsmen currently on crease and bowler spells).
- Support for Duckworth-Lewis-Stern (DLS) rain-interrupted scenarios.
- Integration of live API feeds for real-time match scoring.
- Incorporate historical head-to-head records and pitch conditions.

---

## 👨‍💻 Author / Developer

- **Developer:** IPL Win Predictor Contributors
- **GitHub:** [@your-username](https://github.com/your-username)
