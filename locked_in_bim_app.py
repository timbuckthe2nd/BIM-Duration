
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import cloudpickle


# Load locked-in model and polynomial transformer
model = joblib.load("locked_in_ridge_model.pkl")
poly = joblib.load("locked_in_poly_features.pkl")

# Load feature names
with open("locked_in_feature_columns.txt") as f:
    feature_names = f.read().splitlines()

# App interface
st.title("BIM Coordination Duration Estimator")

start_date = st.date_input("Start Date", value=datetime.today())
scope = st.selectbox("Scope", ["NEW", "RENO", "EXP", "B.O.", "NEW\RENO", "EXP\RENO"])
contract = st.selectbox("Contract Type", ["BB", "DA", "AB"])
building_type = st.selectbox("Building Type", [
    "Healthcare", "Hospitality/Residential", "Industrial/Warehouse",
    "Office", "Shell Space", "Student Facilities", "Multi-Building Resort"
])
sq_ft = st.number_input("Square Footage", min_value=1000, value=50000)
levels = st.number_input("Number of Levels", min_value=1, value=1)

if st.button("Estimate Duration"):
    log_sqft = np.log(sq_ft)
    X_input = dict.fromkeys(feature_names, 0)

    # Populate known fields
    X_input["Log Sq Ft"] = log_sqft
    X_input["Levels"] = levels

    if f"Scope_{scope}" in X_input:
        X_input[f"Scope_{scope}"] = 1
    if f"Contract_{contract}" in X_input:
        X_input[f"Contract_{contract}"] = 1
    if f"BT_{building_type}" in X_input:
        X_input[f"BT_{building_type}"] = 1

    # Interactions
    if "Levels * Log Sq Ft" in X_input:
        X_input["Levels * Log Sq Ft"] = levels * log_sqft
    if "Levels * Scope_NEW" in X_input and scope == "NEW":
        X_input["Levels * Scope_NEW"] = levels
    if "Levels * Contract_BB" in X_input and contract == "BB":
        X_input["Levels * Contract_BB"] = levels
    if "Log Sq Ft * Contract_BB" in X_input and contract == "BB":
        X_input["Log Sq Ft * Contract_BB"] = log_sqft

    # Convert to DataFrame and transform
    X_df = pd.DataFrame([X_input])
    X_poly = poly.transform(X_df)

    prediction = model.predict(X_poly)[0]
    end_date = start_date + timedelta(days=round(prediction))

    st.success(f"Predicted Duration: {round(prediction, 1)} days")
    st.info(f"Predicted End Date: {end_date.strftime('%Y-%m-%d')}")
