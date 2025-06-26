
import streamlit as st
import numpy as np
import datetime

# Hardcoded coefficients from the Ridge model (simplified for demo)
INTERCEPT = 22.1614
COEFFICIENTS = {
    'Log Sq Ft': 67.8822,
    'Levels': 7.3205,
    'Scope_NEW': 48.1697,
    'Scope_RENO': 28.3512,
    'Scope_EXP': 27.0569,
    'Scope_B.O.': 13.9849,
    'Contract_BB': -23.7471,
    'BT_Hospitality/Residential': 34.5246,
    'Levels Scope_NEW': 5.8478,
    'Log Sq Ft Scope_NEW': 25.6414
}

st.title("BIM Coordination Duration Estimator")

# User Inputs
start_date = st.date_input("Start Date", value=datetime.date.today())
scope = st.selectbox("Scope", ["NEW", "RENO", "EXP", "B.O."])
contract = st.selectbox("Contract Type", ["BB"])
building_type = st.selectbox("Building Type", ["Hospitality/Residential"])  # Extend list as needed
sqft = st.number_input("Total Square Feet", min_value=1, step=1)
levels = st.number_input("Number of Levels", min_value=1, step=1)

if st.button("Predict Duration"):
    log_sqft = np.log(sqft)

    # Build feature vector
    features = {
        'Log Sq Ft': log_sqft,
        'Levels': levels,
        f'Scope_{scope}': 1,
        f'Contract_{contract}': 1,
        f'BT_{building_type}': 1,
        f'Levels Scope_{scope}': levels * 1,
        f'Log Sq Ft Scope_{scope}': log_sqft * 1
    }

    # Calculate prediction
    prediction = INTERCEPT
    for feature, coef in COEFFICIENTS.items():
        val = features.get(feature, 0)
        prediction += coef * val

    predicted_end = start_date + datetime.timedelta(days=round(prediction))

    st.success(f"Predicted Coordination Duration: {round(prediction, 1)} days")
    st.success(f"Predicted End Date: {predicted_end.strftime('%B %d, %Y')}")
