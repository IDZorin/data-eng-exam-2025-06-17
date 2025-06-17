from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from etl import load_data, preprocess, train_model, evaluate, upload_results
import os
from dotenv import load_dotenv

load_dotenv()

SCHEDULE = os.getenv("PIPELINE_SCHEDULE", None)

default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=15),
}

with DAG(
    dag_id="breast_cancer_pipeline",
    description="ETL + ML for breast-cancer diagnostic",
    schedule_interval=SCHEDULE,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
) as dag:

    t1 = PythonOperator(
        task_id="load_data",
        python_callable=load_data.run,
    )

    t2 = PythonOperator(
        task_id="preprocess",
        python_callable=preprocess.run,
        op_args=["{{ ti.xcom_pull(task_ids='load_data') }}"],
    )

    t3 = PythonOperator(
        task_id="train_model",
        python_callable=train_model.run,
        op_args=["{{ ti.xcom_pull(task_ids='preprocess') }}"],
    )

    t4 = PythonOperator(
        task_id="evaluate",
        python_callable=evaluate.run,
        op_args=["{{ ti.xcom_pull(task_ids='train_model') }}"],
    )

    t5 = PythonOperator(
        task_id="upload_results",
        python_callable=upload_results.run,
    )

    t1 >> t2 >> t3 >> t4 >> t5
