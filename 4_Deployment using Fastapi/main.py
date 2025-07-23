from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from model_loader import model
import pandas as pd

app = FastAPI()

class InputData(BaseModel):
    total_events: float
    total_purchases: float
    active_days: float


@app.get("/")
def read_root():
    return {"message": "Model API is Live!"}

@app.post("/predict/")
def predict(data: InputData):
    input_df = pd.DataFrame([{
    "total_events": data.total_events,
    "total_purchases": data.total_purchases,
    "active_days": data.active_days
    }])

    prediction = model.predict(input_df)[0]
    return {"prediction": int(prediction)}
