# Airbnb MLOps

Курсовой проект ML/DLOps.
Данные: Inside Airbnb.


## Задача

Выбрана задача регрессии: по характеристикам объявления предсказать цену за ночь (`price`).

## Структура проекта

```
airbnb-mlops/
├── 01_training.ipynb    # EDA, очистка, сравнение моделей, GridSearchCV
├── 02_pipeline.ipynb    # sklearn Pipeline, сохранение и загрузка model.pkl
├── docker/
│   ├── Dockerfile               # образ для обучения
│   ├── api.Dockerfile           # образ для API
│   ├── requirements_docker.txt  # зависимости обучения
│   └── requirements_api.txt     # зависимости API
├── src/
│   └── __init__.py      # для инициализации src как пакета
│   └── data.py          # чтение CSV из S3
│   └── train.py         # обучение Pipeline, сохранение и загрузка model.pkl
│   └── app.py           # FastAPI: POST /predict
├── compose.yaml         # сервисы train и api
├── requirements.txt     # зависимости
├── .env.example         # шаблон переменных окружения
└── README.md
```

## Установка


```bash
git clone https://github.com/nastyaschetinova/airbnb-mlops.git
cd airbnb-mlops
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка доступа к S3

Ключи передаются через переменные окружения и не хранятся в коде. Скопируйте шаблон и заполните ключи:

```bash
cp .env.example .env
```

| Переменная | Описание |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | идентификатор ключа доступа |
| `AWS_SECRET_ACCESS_KEY` | секретный ключ |
| `S3_ENDPOINT_URL` | адрес хранилища, `https://storage.yandexcloud.net` |
| `S3_BUCKET` | имя бакета |
| `S3_KEY` | путь к CSV внутри бакета |


## Запуск ноутбуков

Откройте ноутбуки в VS Code или Jupyter, выберите ядро `.venv` и выполните *Restart → Run All*:


## Docker Batch, Docker API и Docker Compose

1. Скопируйте `.env.example` в `.env` и заполните ключи S3:
   `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_ENDPOINT_URL`, `S3_BUCKET`, `S3_KEY`.
2. Запустите:
   ```bash
   docker compose up --build
   ```
Train: контейнер читает данные из S3, обучает Pipeline, выводит метрики, сохраняет `model.pkl` в Docker volume `model-data` и завершается с кодом 0.
API: стартует только после успешного завершения train, загружает `model.pkl` из того же volume и поднимает API на порту 8000.

### Пример запроса

```bash
curl http://localhost:8000/health
```
или открыть ссылку: http://localhost:8000/docs