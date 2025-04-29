from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor 
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta


with DAG( dag_id = 'House_prices_ETL',description = 'DAG tht make etl' , schedule = '@daily',start_date = datetime(2023,10,1),
         default_args = {'depend_on_past': False},max_active_runs = 1,catchup = False) as dag:
    
    # Define tasks

    #Task 1: Message to indicates the start of th DAG
    satrt_message = BashOperator( task_id = 'start_message', bash_command = "sleep 5 && echo 'ETL starting")

    #Task 2 : Check if there is new data
    check_new_data = SqlSensor( task_id = 'check_new_data', conn_id ='mysql_default',
                                sql = 'SELECT COUNT(*) FROM house_prices WHERE created_at > NOW() - INTERVAL 1 DAY', #Secciona los registros que fueron creados o actualizados en las últimas 24 horas.
                                mode = 'reschedule', timeout = 600, poke_interval = 60, soft_fail = False, trigger_rule = TriggerRule.ALL_SUCCESS)
    
    #Task 3 : Transform data with Python
    transform_data_Python = BashOperator( task_id = 'transform_data', bash_command = "sleep 5 && echo 'Transforming data with PySpark'")

    satrt_message >> check_new_data >> transform_data_Python