# Airflow + LogisticRegression


> Репозиторий-шаблон с ETL + ML-пайплайном под Airflow.
> По умолчанию он скачивает небольшой CSV-датасет, обучает `LogisticRegression`, считает метрики и отправляет артефакты в GCS и кладёт локально в `results/`.
>
> Замените входные данные, модель и параметры — и получите готовый продакшн-пайплайн «из коробки».
>
> **Проверка работоспособности в папке proofs**

---

## 📂 Структура репозитория

```
├── dags/                # DAG Airflow «breast_cancer_pipeline»
├── etl/                 # независимые модули: load → preprocess → train → evaluate → upload
├── results/             # артефакты (csv / pkl / json) создаются сюда
├── logs/                # runtime-логи (pipeline_<timestamp>.log)
├── proofs/              # скриншоты UI / GCS (для отчёта)
├── keys/                # GCP service-account json (НЕ коммитим!)
├── docker-compose.yml   # webserver + scheduler
├── Dockerfile           # образ со всеми зависимостями
├── requirements.txt
├── makefile             # локальный запуск без Docker/Airflow
├── .env                 # все переменные окружения
└── README.md            # вы здесь
```

---

## ⚙️ Конфигурация

| Ключ                             | Где задаётся                      | Что вставить                                                                                                                                                                     |
| -------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GCP_PROJECT`                    | `.env`                            | ID вашего проекта в Google Cloud                                                                                                                                                 |
| `GCS_BUCKET`                     | `.env`                            | имя бакета                                                                                                                                                                       |
| `GCS_PREFIX`                     | `.env`                            | префикс внутри бакета (по умолчанию `breast_cancer/`)                                                                                                                            |
| `GOOGLE_APPLICATION_CREDENTIALS` | `.env` **и** `docker-compose.yml` | путь к `.json`-ключу сервис-аккаунта. **Важно:** путь может быть относительным  |
| `PIPELINE_SCHEDULE`              | `.env`                            | CRON-выражение для DAG (если пустое - запуск в ручную).                                                                                                              |

**Hardcodes**

* `dags/pipeline_dag.py` — `start_date=datetime(2025, 1, 1)` → поправьте при необходимости.
* `etl/config.py` — содержит URL примера датасета; замените на свой источник.
* В `logger_setup.py` имя лога фиксированное, но путь формируется автоматически.
* БД Airflow (`AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`) сейчас на `sqlite:///…` — для продакшена смените на PostgreSQL/MySQL.
* Исполнитель (`SequentialExecutor`) — то же самое: в prod переключитесь на `LocalExecutor`, `CeleryExecutor`, etc.

---

## 🚀 Запуск

### 1. Локальный с makefile

```bash
# создаём/активируем виртуальное окружение и ставим зависимости
make setup

# прогоняем всю цепочку: результаты лягут в results/, логи — в logs/
make run
```

### 2. Docker

```bash
# 0) заполнить .env и убедиться, что ключ лежит в keys/
docker compose up --build
```

* Airflow UI: [http://localhost:8080](http://localhost:8080), логин/пароль `admin` / `admin`.
* DAG **breast\_cancer\_pipeline** либо запуск ручной Run.

**Как изменить расписание**

1. `PIPELINE_SCHEDULE="0 3 * * *"` (пример: каждый день в 03:00 UTC) в `.env`.
2. Перезапустите контейнеры — DAG автоматически подхватит CRON.

---


## 💡 Идеи для развития

1. **Более гибкое логирование** — именовать файлы `pipeline_<dag_run_id>.log`, складывать в S3 / Stackdriver.
2. **Data validation** (`great_expectations`, `pandera`) до обучения модели.
3. **Unit-тесты** на каждый ETL-модуль (`pytest` + fixtures).
4. **CI/CD** — автопубликация Docker-образа, деплой DAG через Helm-chart в Airflow-Kubernetes.
5. **Визуализация метрик** → сохранённые JSON можно прокинуть в Grafana / Loki.

## ⚠️ Потенциальные проблемы

* **load\_data**
  Сетевые сбои — timeout, 404. Сейчас вызывается `requests.get` с `timeout=30` и `raise_for_status()`. В дальнейшем лучше добавить retry c экспоненциальной задержкой.
* **preprocess**
  Неверная схема CSV, неожиданные `NaN`. Колонки переименовываются явно, но валидацию схемы перед масштабированием стоит добавить.
* **train\_model**
  `LogisticRegression` может не сойтись 
  `ConvergenceWarning`, при необходимости увеличивать `max_iter`.
* **upload\_results**

  * Не найден JSON-ключ → `DefaultCredentialsError`.
  * 403 «Billing account disabled» или нехватка IAM-прав на bucket.
    Путь к ключу приводится к абсолютному, есть `early-exit`, если `GCS_BUCKET` пуст. Для продакшена полезно заранее проверять права и/или слать алерт в месенджер.
* **Инфраструктура Airflow**

  * **SQLite как metadata-БД**: Airflow прямо предупреждает — *«Do not use SQLite as metadata DB in production»*. В проде лучше перейти на PostgreSQL.
  * **SequentialExecutor**: аналогично — годится лишь для локальных тестов; в продакшене лучше `LocalExecutor`, `CeleryExecutor` или `KubernetesExecutor`.
