import os
import pandas as pd
import mlflow
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# MLflow configuration
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
REGISTERED_MODEL_NAME = "iris_rf_model"

# Pydantic models for request and response
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class Prediction(BaseModel):
    prediction: int

# Create FastAPI app
app = FastAPI()

# Load the model from MLflow Model Registry
try:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    model = mlflow.pyfunc.load_model(f"models:/{REGISTERED_MODEL_NAME}/latest")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/predict", response_model=Prediction)
def predict(iris_input: IrisInput):
    """Predict the class for a single iris flower."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Create a pandas DataFrame from the input
        input_df = pd.DataFrame([iris_input.dict()])

        # Make a prediction
        prediction = model.predict(input_df)

        # Return the prediction
        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
