#import pymysql
from airflow.models.baseoperator import BaseOperator
from datetime import datetime , date
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect
