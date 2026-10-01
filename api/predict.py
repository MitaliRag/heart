import os
import joblib
import pandas as pd

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model = joblib.load(
    os.path.join(BASE_DIR, "model", "model.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "model", "scaler.pkl")
)

features = joblib.load(
    os.path.join(BASE_DIR, "model", "features.pkl")
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Heart Disease Prediction API is running"
    }


@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    df = pd.get_dummies(df)

    df = df.reindex(
        columns=features,
        fill_value=0
    )

    scaled_data = scaler.transform(df)

    prediction = model.predict(
        scaled_data
    )[0]

    probability = model.predict_proba(
        scaled_data
    )[0][1]

    if prediction == 1:
        result = "Heart Disease Detected"
    else:
        result = "No Heart Disease Detected"

    return {
        "success": True,
        "result": result,
        "prediction": int(prediction),
        "probability": round(
            probability * 100,
            2
        )
    }