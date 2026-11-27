"""FastAPI-сервис: предсказание цены за ночь для объявления Airbnb"""


import os
import pickle
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

MODEL_PATH = Path(os.getenv("MODEL_PATH", "artifacts/model.pkl"))

FEATURES = [
    "latitude", "longitude", "accommodates", "bathrooms", "bedrooms", "beds", "minimum_nights", "neighbourhood_cleansed", "property_type", "room_type",
]


class Listing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    latitude: float = Field(examples=[51.5141])
    longitude: float = Field(examples=[-0.1768])
    accommodates: int = Field(ge=1, examples=[4])
    bathrooms: float | None = Field(default=None, ge=0, examples=[1.0])
    bedrooms: float | None = Field(default=None, ge=0, examples=[2.0])
    beds: float | None = Field(default=None, ge=0, examples=[2.0])
    minimum_nights: float = Field(ge=1, examples=[2])
    neighbourhood_cleansed: str = Field(examples=["Westminster"])
    property_type: str = Field(examples=["Entire rental unit"])
    room_type: str = Field(examples=["Entire home/apt"])


class Prediction(BaseModel):
    price: float
    currency: str = "GBP"


@asynccontextmanager
async def lifespan(app: FastAPI):
    with MODEL_PATH.open("rb") as f:
        app.state.model = pickle.load(f)
    print(f"Модель загружена из {MODEL_PATH}")
    yield


app = FastAPI(title="Airbnb London Price API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": hasattr(app.state, "model")}


@app.post("/predict", response_model=Prediction)
def predict(listing: Listing):
    X = pd.DataFrame([listing.model_dump()], columns=FEATURES)
    # TransformedTargetRegressor сам делает expm1 -> ответ уже в фунтах
    price = float(app.state.model.predict(X)[0])
    return {"price": round(price, 2)}