#import pymysql
from airflow.models.baseoperator import BaseOperator
from datetime import datetime , date
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sklearn.model_selection import KFold


class Transform_Python(BaseOperator):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def connection(self):
        """This methos creates a connection with the  db with pandas"""
        host = 'mysql'
        port='3306'
        user = 'house'
        password = 'house'
        db = 'house'
        try:
            connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
            engine = create_engine(connection_string)
        
        except Exception as e:
            self.log.error(f"Error creating connection: {e}")
            raise

        return engine
    
    def ETL(self):
         
        """This method is used to transform the data from the db and the save in a datawarehouse"""

        engine = self.connection() 

        inspector = inspect(engine)
        df = pd.reead_sql_table('house_DataLake', con=engine)
        
        #Get inecesay columns that have more than 80% of ZEROS or NULLS
        Drop_columns = self.columnas_ceros(df)
        Drop_columns.extend(self.columnas_nulos(df))

        #Drop the columns
        
        #C reate a new df eith onlu numeric columns
        df_numeric = df.select_dtypes(include=['int64', 'float64'])




    #Get the columns that have more than 80% of ZEROS
    def columnas_ceros(dataframe):

        train_columns = dataframe.columns

        columnas = [col for col in train_columns if (dataframe[col]==0).sum() > 650 ]

        return columnas
    
    #Get the columns that have more than 80% of NULLS
    def columnas_nulos(dataframe):

        train_columns = dataframe.columns

        columnas = [col for col in train_columns if dataframe[col].isna().sum() > 650 ]

        return columnas
    
    def encoding(self,df):
        """This method is used to encode the categorical columns"""
        #Get the categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        




