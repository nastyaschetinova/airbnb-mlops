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
│   └── Dockerfile       #коробка
│   └── requirements_docker.txt # зависимосим для Dockera
│   └── .dockerignore.   # правила сборки
├── src/
│   └── __init__.py      # для инициализации src как пакета
│   └── data.py          # чтение CSV из S3
│   └── train.py         # обучение Pipeline, сохранение и загрузка model.pkl
├── compose.yaml         # инструкция по запуску Dockerfile
├── requirements.txt     # зависимости
├── .env.example         # шаблон переменных окружения
├── .gitignore           # что не берем в гит
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


## Обучение в Docker

1. Скопируйте `.env.example` в `.env` и заполните ключи S3:
   `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_ENDPOINT_URL`, `S3_BUCKET`, `S3_KEY`.
2. Запустите обучение:
   ```bash
   docker compose up --build train
   ```
   Контейнер читает данные из S3, обучает Pipeline, выводит метрики, сохраняет `model.pkl` в Docker volume `model-data` и завершается с кодом 0.
