"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""

import logging
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

def my_python_function(num):
    result = num ** 2
    logging.info(result)
    return result

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

dag = DAG(dag_id='tutorial3', default_args=default_args, schedule_interval=timedelta(days=1))

process_start = DummyOperator(dag=dag, task_id='process_start')
process_end = DummyOperator(dag=dag, task_id='process_end')

for i in range(5):
    task = DummyOperator(dag=dag, task_id='task_{}'.format(i))
    process_start >> task
    for j in range(2):
        subtask = PythonOperator(
            dag=dag,
            task_id='subtask_{}_{}'.format(i,j),
            python_callable=my_python_function,
            op_kwargs={'num': i}
        )
        if j == 1:
            task >> subtask >> process_end
        else:
            task >> subtask

