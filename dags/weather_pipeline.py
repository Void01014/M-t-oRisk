from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="meteorisK_pipeline",
    start_date=datetime(2026, 9, 17),
    schedule="@daily",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract_weather",
        bash_command="cd /opt/meteorisK && python extraction/extract_weather.py",
    )

    silver = BashOperator(
        task_id="transform_to_silver",
        bash_command="cd /opt/meteorisK && python transformation/to_silver.py",
    )

    gold = BashOperator(
        task_id="transform_to_gold",
        bash_command="cd /opt/meteorisK && python transformation/to_gold.py",
    )

    load = BashOperator(
        task_id="load_to_postgres",
        bash_command="cd /opt/meteorisK && python load/load_gold.py",
    )

    extract >> silver >> gold >> load