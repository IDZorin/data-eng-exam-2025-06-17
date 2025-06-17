FROM apache/airflow:2.9.1-python3.10

USER root
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY dags /opt/airflow/dags
COPY etl  /opt/airflow/etl
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
