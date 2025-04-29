from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor 
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta