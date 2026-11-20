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
├── src/
│   └── data.py          # чтение CSV из S3
├── requirements.txt     # зависимости
├── .env.example         # шаблон переменных окружения
└── README.md
```

## Установка

Python 3.12+.

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


## Запуск

Откройте ноутбуки в VS Code или Jupyter, выберите ядро `.venv` и выполните *Restart → Run All*:
