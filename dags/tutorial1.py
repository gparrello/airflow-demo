"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2015, 6, 1),
    # 'end_date': datetime(2016, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(dag_id='tutorial1', default_args=default_args, schedule_interval=timedelta(days=1))

process_start = DummyOperator(dag=dag, task_id='process_start')
task1 = DummyOperator(dag=dag, task_id='task1')
process_end = DummyOperator(dag=dag, task_id='process_end')

process_start >> task1 >> process_end

