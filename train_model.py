import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/heart.csv")

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# Target column
target = "target"

if target not in df.columns:
    raise ValueError("Column 'target' not found in heart.csv")

# Features and target
X = df.drop(columns=[target])
y = df[target]

# Convert categorical data if present
X = pd.get_dummies(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# Accuracy
prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Model Accuracy:", accuracy)

# Create model folder
os.makedirs("model", exist_ok=True)

# Save model
joblib.dump(model, "model/model.pkl")

# Save scaler
joblib.dump(scaler, "model/scaler.pkl")

# Save feature names
joblib.dump(
    pd.read_csv("data/heart.csv")
    .drop(columns=[target])
    .pipe(pd.get_dummies)
    .columns.tolist(),
    "model/features.pkl"
)

print("Model files created successfully!")
