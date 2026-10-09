
import os
import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Project root folder
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = os.path.join(BASE_DIR, "model")

# Load trained files
try:
    model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    features = joblib.load(os.path.join(MODEL_DIR, "features.pkl"))
except Exception as error:
    raise RuntimeError(
        f"Could not load model files from {MODEL_DIR}: {error}"
    ) from error

app = FastAPI(title="Heart Disease Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Heart Disease Prediction API is running"}


@app.get("/features")
def get_features():
    return {
        "features": list(features),
        "numeric_features": list(features),
    }


@app.post("/predict")
def predict(data: dict):
    try:
        missing_features = [
            feature for feature in features
            if feature not in data
        ]

        if missing_features:
            raise HTTPException(
                status_code=400,
                detail=f"Missing features: {missing_features}",
            )

        # Match the model's expected feature columns
        df = pd.DataFrame([data])
        df = pd.get_dummies(df)
        df = df.reindex(columns=features, fill_value=0)

        scaled_data = scaler.transform(df)
        prediction = int(model.predict(scaled_data)[0])

        probability = None
        if hasattr(model, "predict_proba"):
            probability = round(
                float(model.predict_proba(scaled_data)[0][1]) * 100,
                2,
            )

        result = (
            "Heart Disease Detected"
            if prediction == 1
            else "No Heart Disease Detected"
        )

        return {
            "success": True,
            "result": result,
            "prediction": prediction,
            "probability": probability,
            "risk_probability": (
                probability / 100
                if probability is not None
                else None
            ),
            "note": (
                "This is a machine-learning prediction, "
                "not a medical diagnosis."
            ),
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}",
        )

