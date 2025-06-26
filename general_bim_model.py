
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures

# Load your dataset
df = pd.read_excel("your_dataset.xlsx")  # Replace with actual path

# Preprocessing
df["Log Sq Ft"] = np.log(df["Sq Ft"])
df["Levels"] = df["Levels"].astype(float)
df["Actual_Duration"] = (pd.to_datetime(df["BIM End Date"]) - pd.to_datetime(df["BIM Start Date"])).dt.days

# One-hot encoding
X = pd.get_dummies(df[["Scope", "Contract", "Building Type"]], prefix=["Scope", "Contract", "BT"])
X["Log Sq Ft"] = df["Log Sq Ft"]
X["Levels"] = df["Levels"]

# Interaction terms
X["Levels Scope_NEW"] = X.get("Scope_NEW", 0) * df["Levels"]
X["Log Sq Ft Scope_NEW"] = X.get("Scope_NEW", 0) * df["Log Sq Ft"]

# Polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Target
y = df["Actual_Duration"]

# Train Ridge Regression model
model = Ridge(alpha=1.0)
model.fit(X_poly, y)

# Predict
df["Predicted_Duration"] = model.predict(X_poly)
df["Percent_Error"] = ((df["Predicted_Duration"] - y) / y * 100).round(2)

# Output predictions
print(df[["Project Name", "Predicted_Duration", "Actual_Duration", "Percent_Error"]])
