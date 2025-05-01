import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

class model():

    def __init__(self):
        pass

    def connection():
        """This methos creates a connection with the  db with pandas"""
        host = 'localhost'
        port=3308
        user = 'house'
        password = 'house'
        db = 'house'
        try:
            connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
            engine = create_engine(connection_string)
        
        except Exception as e:
            print((f"Error creating connection: {e}"))
            raise

        return engine 