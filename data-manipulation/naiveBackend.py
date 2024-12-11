from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error
from sklearn.impute import SimpleImputer
import json

# Start with uvicorn naiveBackend:app --reload
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

model = None
lung_model = None
features = []
target = "CancerIncidence"
df = pd.read_csv("combined_dataset.csv")
lung_df = pd.read_csv("Lung_dataset.csv")

features = ["BingeDrinking", "CoronaryHeartDisease", "Diabetes",
            "Asthma", "Obesity", "BelowPoverty", "Smoking"]  

def preprocess_data(X):
    imputer = SimpleImputer(strategy="mean")  
    X_imputed = imputer.fit_transform(X)
    return pd.DataFrame(X_imputed, columns=X.columns)

def load_and_prepare_data():
    global features
    X = df[[ "BelowPoverty","Diabetes"]]
    #X = df[features]
    y = df[target]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model():
    global model
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    X_train = preprocess_data(X_train)
    X_test = preprocess_data(X_test)
    print("x test:\n", X_test)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print(f"Liver County Incidence Linear Regression Validation - MSE: {mse}, RMSE: {np.sqrt(mse)}, R²: {r2}, MAE: {mae}, MAPE: {mape}%")
    return {"mse": mse, "rmse": np.sqrt(mse), "r2": r2, "mae": mae, "mape": mape}
   
    
def load_and_prepare_data_lung():
    global features
    X = lung_df[["Smoking"]]
    X = lung_df[features]
    y = lung_df["LungCancerIncidence"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_lung_model():
    global lung_model
    X_train, X_test, y_train, y_test = load_and_prepare_data_lung()
    X_train = preprocess_data(X_train)
    X_test = preprocess_data(X_test)
    lung_model = LinearRegression()
    lung_model.fit(X_train, y_train)
    y_pred = lung_model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print(f"Lung County Incidence Linear Regression Validation - MSE: {mse}, RMSE: {np.sqrt(mse)}, R²: {r2}, MAE: {mae}, MAPE: {mape}%")
    return {"mse": mse, "rmse": np.sqrt(mse), "r2": r2, "mae": mae, "mape": mape}



# API endpoint to retrain the model
@app.post("/retrain")
def retrain():
    train_model()
    return {"message": "Model retrained successfully"}

# API endpoint for predictions
class PredictionInput(BaseModel):
    #AirQuality: float
    BelowPoverty: float
    Diabetes: float
@app.post("/predict/")
def predict(input_data: PredictionInput):
    input_df = pd.DataFrame([input_data.dict()])
    print(input_df)
    # Model prediction
    try:
        prediction = model.predict(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    return {
        "prediction": float(prediction[0]),  # Linear Regression outputs a single continuous value
    }

class PredictionInput(BaseModel):
    Smoking: float
    Asthma: float
    Obesity: float
    #CoronaryHeartDisease: float
@app.post("/lung/predict/")
def predict(input_data: PredictionInput):
    input_df = pd.DataFrame([input_data.dict()])
    print(input_df)
    # Model prediction
    try:
        prediction = lung_model.predict(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    return {
        "prediction": float(prediction[0]),  # Linear Regression outputs a single continuous value
    }


@app.get("/correlations")
def get_highly_correlated_factors(threshold: float = 0.2):
    """
    Calculate correlations and return highly correlated factors with cancer incidence.
    :param threshold: Correlation threshold (default is 0.5)
    """
    required_columns = ["BingeDrinking", "CoronaryHeartDisease", "Diabetes",
                        "Asthma", "Obesity", "BelowPoverty", "Smoking", "CancerIncidence"]
    df_copy = df[required_columns]
    df_copy = df_copy.select_dtypes(include=["float64", "int64"])
    correlation_matrix = df_copy.corr()
    print("correlation\n", correlation_matrix)
    # Extract correlations with the target variable
    correlations = correlation_matrix[target].drop(target)

    # Take the absolute value of correlations
    abs_correlations = correlations.abs()

    # Filter factors with correlation above the threshold
    highly_correlated = abs_correlations[abs_correlations >= threshold].sort_values(ascending=False)

    return {"highly_correlated_factors": highly_correlated.to_dict()}

@app.get("/lung/correlations")
def get_highly_correlated_factors(threshold: float = 0.2):
    """
    Calculate correlations and return highly correlated factors with cancer incidence.
    :param threshold: Correlation threshold (default is 0.5)
    """
    required_columns = ["BingeDrinking", "CoronaryHeartDisease", "Diabetes",
                        "Asthma", "Obesity", "BelowPoverty", "Smoking", "LungCancerIncidence"]
    df_copy = lung_df[required_columns]
    df_copy = df_copy.select_dtypes(include=["float64", "int64"])
    correlation_matrix = df_copy.corr()
    print("correlation\n", correlation_matrix)
    # Extract correlations with the target variable
    correlations = correlation_matrix["LungCancerIncidence"].drop("LungCancerIncidence")

    # Take the absolute value of correlations
    abs_correlations = correlations.abs()

    # Filter factors with correlation above the threshold
    highly_correlated = abs_correlations[abs_correlations >= threshold].sort_values(ascending=False)

    return {"highly_correlated_factors": highly_correlated.to_dict()}

@app.get("/liver/highest-cancer-rate")
def get_state_with_highest_cancer_rate():
    """
    Finds the state with the highest average cancer rate and compares it to the average rate across all states.
    Assumes the dataset has columns 'State' and 'CancerIncidence'.
    """
    try:
        # Group data by 'State' and calculate the mean of 'CancerIncidence'
        grouped = df.groupby("State")["CancerIncidence"].mean()

        # Find the state with the highest average cancer rate
        state_with_highest_rate = grouped.idxmax()
        highest_rate = grouped.max()

        # Calculate the overall average cancer rate across all states
        overall_average_rate = grouped.mean()

        return {
            "state_with_highest_rate": state_with_highest_rate,
            "highest_average_rate": highest_rate,
            "overall_average_rate": overall_average_rate
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {e}")
    
@app.get("/lung/highest-cancer-rate")
def get_state_with_highest_cancer_rate():
    """
    Finds the state with the highest average cancer rate and compares it to the average rate across all states.
    Assumes the dataset has columns 'State' and 'CancerIncidence'.
    """
    try:
        # Group data by 'State' and calculate the mean of 'CancerIncidence'
        grouped = lung_df.groupby("State")["LungCancerIncidence"].mean()

        # Find the state with the highest average cancer rate
        state_with_highest_rate = grouped.idxmax()
        highest_rate = grouped.max()

        # Calculate the overall average cancer rate across all states
        overall_average_rate = grouped.mean()

        return {
            "state_with_highest_rate": state_with_highest_rate,
            "highest_average_rate": highest_rate,
            "overall_average_rate": overall_average_rate
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {e}")

    
@app.get("/overlay-data")
def get_overlay_data(factor: str = Query(..., description="Factor to overlay")):
    if factor not in features:
        return {"error": f"Invalid factor. Available factors: {', '.join(features)}"}
    
    # Prepare data with countyFIPS
    data = df[["CountyFIPS", "County", "State", factor]].dropna().to_dict(orient="records")
    # print(data)
    return {"factor": factor, "data": data}

# Initialize and train the model on startup
train_model()
train_lung_model()