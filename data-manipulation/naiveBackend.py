from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
#start with uvicorn naive:app --reload
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
# Placeholder for model and data
model = None
features = []
target = "CancerIncidence"

# Example dataset loading and preprocessing
def load_and_prepare_data():
    # Combine your cancer incidence and factors dataset here
    df = pd.read_csv("combined_dataset.csv")
    global features

    # Define features and target column
    features = ["BingeDrinking", "CoronaryHeartDisease", "Diabetes"]  # Replace with actual factor names
    X = df[features]
    y = df[target]
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
def train_model():
    global model
    X_train, _, y_train, _ = load_and_prepare_data()
    model = GaussianNB()
    model.fit(X_train, y_train)

# API endpoint to retrain the model
@app.post("/retrain")
def retrain():
    train_model()
    return {"message": "Model retrained successfully"}

# API endpoint for predictions
class PredictionInput(BaseModel):
    BingeDrinking: float
    CoronaryHeartDisease: float
    Diabetes: float

@app.post("/predict/")
def predict(input_data: PredictionInput):
    # Assuming `model` is a trained Naive Bayes model
    input_df = pd.DataFrame([input_data.dict()])

    # Model prediction
    prediction = model.predict(input_df)  # This is returning a list of strings
    probability = model.predict_proba(input_df).max(axis=1)

    print("Prediction raw output:", prediction)  # Debugging
    print("Probability raw output:", probability)  # Debugging

    # Convert prediction to a numeric type
    try:
        prediction_value = float(prediction[0])  # Convert to a float
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Invalid prediction format: {e}")

    return {
        "prediction": prediction_value,
        "probability": float(probability[0]),  # Ensure probability is a float
    }
    
# Initialize and train the model on startup
train_model()
