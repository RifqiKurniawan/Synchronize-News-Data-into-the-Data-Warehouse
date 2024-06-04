import airflow 
from datetime import timedelta 
from airflow import DAG 
from datetime import datetime, timedelta 
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import pendulum


local_tz = pendulum.timezone("Asia/Jakarta")

default_args = {
    "owner": "rifqik",
    "depends_on_past": False,
    # "email":["Rifqi.acim@gmail.co.id"],
    "start_date": datetime(2024, 6, 3),  # yyyy, M, D
    "retries": 0,
    "retry_delay": timedelta(minutes=2),
}

dag= DAG(
    dag_id="SYNC_DATA_1_HOUR",
    tags=["1_HOUR","SYNC_DATA"],
    default_args=default_args,    
    catchup=False,
    schedule_interval="0 */1 * * *",
    start_date=pendulum.datetime(2024, 3, 5,0,0,0, tz=local_tz),
    )

def path_query(path_job, job):
    with open(f'{path_job}sql/{job}.sql') as query:
        query = query.read()
    return query      


# path_job=f'/home/devsmapp/.local/lib/python3.9/site-packages/airflow/source_dags/damen/project/sharp/python/email/send_email_error_sync.py'
sync_id_news_postgres_to_oracle = SSHOperator(
                            task_id='POSTGRES_ID_NEWS',
                            ssh_conn_id= 'PYTHON',
                            cmd_timeout=None,
                            command=f'python3 /opt/source_spark/DAMEN/SHARP/PROJECT/OTHERS/Extract_ID.py', 
                            dag = dag
                          )

sync_postgres_to_oracle = SSHOperator(
                            task_id='INGESTION_POSTGRES',
                            ssh_conn_id= 'PYTHON',
                            cmd_timeout=None,
                            command=f'python3 /opt/source_spark/DAMEN/SHARP/PROJECT/OTHERS/Extract_News.py', 
                            dag = dag
                          )

sync_process_oracle = SQLExecuteQueryOperator(
                            task_id='SYNC_PROCESS_ORACLE',
                            conn_id= 'ORACLE',
                            sql = path_query('/home/devsmapp/.local/lib/python3.9/site-packages/airflow/source_dags/damen/project/sharp/python/', 'USP_SYNC_TR_NEWS'),
                            autocommit ='True',
                            dag = dag
                          )

             
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)

start >> [sync_postgres_to_oracle,sync_id_news_postgres_to_oracle] >> sync_process_oracle >> end
