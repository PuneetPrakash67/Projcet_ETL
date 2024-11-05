from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from reddit_etl import run_reddit_etl  # Ensure this import is correct

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),  # or a fixed date like days_ago(1)
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'AI_PROJECT',#Your DAG NAME#
    default_args=default_args,
    description='DAG for Reddit ETL process!',
    schedule_interval=None,
) as dag:

    run_etl = PythonOperator(
        task_id='complete_reddit_etl',
        python_callable=run_reddit_etl,
    )
