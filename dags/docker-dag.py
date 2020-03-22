from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['thibauld.croonenborghs@tomtom.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'execution_timeout': timedelta(minutes=15),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

START_DATE = datetime(2020, 1, 1, 0, 30, 0)
DAG_NAME = 'Airflow_docker_example'


with DAG(
    dag_id=DAG_NAME,
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1,
    start_date=START_DATE,
    catchup=False
) as dag:

    kick_off_dag = DummyOperator(task_id='kick_off_dag')

    download = DockerOperator(
        task_id='running_download',
        image='airflow-example:latest',
        api_version='auto',
        auto_remove=True,
        command="/docker-entrypoint.sh run-download",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        dag=dag
    )

    preprocessing = DockerOperator(
        task_id='running_preprocessing',
        image='airflow-example:latest',
        api_version='auto',
        auto_remove=True,
        command="/docker-entrypoint.sh run-preprocessing",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        dag=dag
    )

    processing = DockerOperator(
        task_id='running_processing',
        image='airflow-example:latest',
        api_version='auto',
        auto_remove=True,
        command="/docker-entrypoint.sh run-processing",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        dag=dag
    )

    kick_off_dag >> download >> preprocessing >> processing
