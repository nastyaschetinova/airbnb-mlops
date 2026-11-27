"""Обучение модели цены Airbnb — перенос 02_pipeline.ipynb

Шаги: чтение CSV из S3 -> фильтрация цены -> train/test -> sklearn Pipeline
-> метрики на test -> сохранение model.pkl и metrics.json.

Запуск локально:  python -m src.train
Запуск в Docker:  docker compose up --build train

Переменные окружения:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY  — ключи S3 (boto3 читает их сам)
    S3_BUCKET, S3_KEY                          — где лежит CSV
    S3_ENDPOINT_URL                            — необязательно, по умолчанию Yandex Object Storage
    MODEL_PATH                                 — куда сохранить модель (по умолчанию artifacts/model.pkl)
"""

import json
import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (
    mean_absolute_error, median_absolute_error, root_mean_squared_error, r2_score,
)

from src.data import read_s3_csv

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

RANDOM_STATE = 42
PRICE_MAX = 1000
TARGET = "price"
NUM_COLS = ["latitude", "longitude", "accommodates", "bathrooms", "bedrooms", "beds", "minimum_nights"]
CAT_COLS = ["neighbourhood_cleansed", "property_type", "room_type"]


BEST_PARAMS = {
    "l2_regularization": 5.0,
    "learning_rate": 0.03,
    "max_leaf_nodes": 31,
    "min_samples_leaf": 100,
}

MODEL_PATH = Path(os.getenv("MODEL_PATH", "artifacts/model.pkl"))


def load_data() -> pd.DataFrame:
    missing = [name for name in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "S3_BUCKET", "S3_KEY")
               if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Не заданы переменные окружения: {', '.join(missing)}")
    return read_s3_csv(os.environ["S3_BUCKET"], os.environ["S3_KEY"])


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Убираем выбросы дороже £1000 — как в ноутбуке"""
    n0 = len(df)
    df = df[(df[TARGET] > 0) & (df[TARGET] <= PRICE_MAX)].reset_index(drop=True)
    print(f"Фильтр цены: было {n0}, осталось {len(df)} ({len(df) / n0:.1%})")
    return df


def build_pipeline() -> Pipeline:
    prepare = ColumnTransformer([
        ('numbers', SimpleImputer(strategy='median'), NUM_COLS),
        ('category', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['neighbourhood_cleansed', 'room_type']),
        ('property_type', OneHotEncoder(handle_unknown='infrequent_if_exist', sparse_output=False, min_frequency=20), ['property_type'])
    ])

    return Pipeline([
        ('preprocess', prepare),
        ('model', TransformedTargetRegressor(
            regressor=HistGradientBoostingRegressor(max_iter=500, random_state=RANDOM_STATE, **BEST_PARAMS), func=np.log1p, inverse_func=np.expm1,
        )),
    ])


def main() -> None:
    df = clean(load_data())

    X = df[NUM_COLS + CAT_COLS]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    print(f"train: {X_train.shape}, test: {X_test.shape}")

    pipe = build_pipeline()
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)

    metrics = {
        "MAE": round(float(mean_absolute_error(y_test, pred)), 3),
        "MedianAE": round(float(median_absolute_error(y_test, pred)), 3),
        "RMSE": round(float(root_mean_squared_error(y_test, pred)), 3),
        "R2": round(float(r2_score(y_test, pred)), 3),
    }
    print(json.dumps(metrics, indent=2))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_PATH.open("wb") as f:
        pickle.dump(pipe, f)
    (MODEL_PATH.parent / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(f"Модель сохранена: {MODEL_PATH}")


if __name__ == "__main__":
    main()