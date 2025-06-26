
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# --- Embedded model coefficients (locked-in) ---
intercept = 4234.6749

coefs = {
    "Scope_NEW": -46.2768,
    "Contract_BB": 0.0,
    "BT_Hospitality/Residential": -1.2618,
    "Log Sq Ft": -106.9567,
    "Levels": -8.3843,
    "Levels * Log Sq Ft": -127.2351,
    "Levels * Scope_NEW": -58.5132,
    "Levels * Contract_BB": -8.3843,
    "Log Sq Ft * Contract_BB": -106.9567
}

def get_features(scope, contract, building_type, log_sqft, levels):
    features = {
        "Scope_NEW": 1 if scope == "NEW" else 0,
        "Contract_BB": 1 if contract == "BB" else 0,
        f"BT_{building_type}": 1,
        "Log Sq Ft": log_sqft,
        "Levels": levels,
        "Levels * Log Sq Ft": levels * log_sqft,
        "Levels * Scope_NEW": levels if scope == "NEW" else 0,
        "Levels * Contract_BB": levels if contract == "BB" else 0,
        "Log Sq Ft * Contract_BB": log_sqft if contract == "BB" else 0,
    }
    return features

st.title("📐 BIM Coordination Duration Estimator (Offline Model)")

start_date = st.date_input("Start Date", value=datetime.today())
scope = st.selectbox("Scope", ["NEW", "RENO", "EXP", "B.O."])
contract = st.selectbox("Contract Type", ["BB", "DA", "AB"])
building_type = st.selectbox("Building Type", [
    "Healthcare", "Hospitality/Residential", "Industrial", "Office", "Shell Space", "Student Facilities", "Multi-Building Resort"
])
sq_ft = st.number_input("Square Footage", min_value=1000, value=50000)
levels = st.number_input("Number of Levels", min_value=1, value=1)

if st.button("Estimate Duration"):
    log_sqft = np.log(sq_ft)
    feats = get_features(scope, contract, building_type, log_sqft, levels)

    prediction = intercept + sum(coefs.get(k, 0) * v for k, v in feats.items())
    end_date = start_date + timedelta(days=round(prediction))

    st.success(f"🕒 Estimated Duration: {round(prediction)} days")
    st.info(f"📅 Estimated End Date: {end_date.strftime('%Y-%m-%d')}")
