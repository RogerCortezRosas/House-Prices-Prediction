from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor 
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import sys
from airflow.operators.python_operator import PythonOperator


from pathlib import Path

# Añade el directorio Proyecto/ al path de Python
sys.path.append(str(Path(__file__).parent.parent))

from scripts.transform import Transform_Python


with DAG( dag_id = 'House_prices_ETL',description = 'DAG tht make etl' , schedule = '@daily',start_date=datetime(2024,4,7),end_date=datetime(2024,4,20),
         default_args = {'depend_on_past': False},max_active_runs = 1,catchup = True) as dag:
    #Airflow intentará "ponerse al día" (catch up) ejecutando el DAG para cada intervalo de tiempo programado que se perdió desde la start_date hasta la fecha actual..\
    
    # Define tasks

    #Task 1: Message to indicates the start of th DAG
    satrt_message = BashOperator( task_id = 'start_message', bash_command = 'sleep 5 && echo "ETL starting"')

    #Task 2 : Check if there is new data
    check_new_data = SqlSensor( task_id = 'check_new_data', conn_id ='mysql_default',
                                sql = 'SELECT COUNT(Id) FROM house_DataLake WHERE (SELECT COUNT(Id) FROM house_DataLake) > 1', #Secciona los registros que fueron creados o actualizados en las últimas 24 horas.
                                mode = 'reschedule', timeout = 600, poke_interval = 60, soft_fail = False,depends_on_past = False, trigger_rule = TriggerRule.ALL_SUCCESS)
    
    #Task 3 : Transform data with Python
    transform_data_Python = Transform_Python( task_id = 'transform_data_Python',depends_on_past = False, trigger_rule = TriggerRule.ALL_SUCCESS)

    satrt_message >> check_new_data >> transform_data_Python