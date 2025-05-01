#import pymysql
from airflow.models.baseoperator import BaseOperator
from datetime import datetime , date
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sklearn.model_selection import KFold
from sklearn.preprocessing import OrdinalEncoder
import numpy as np

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
    
    def load(self, df):
        """This method is used to load the data into the db"""
        engine = self.connection()
        
        try:
            #Load the data into the db
            df.to_sql('house_WareHouse', con=engine, if_exists='append', index=False)
            self.log.info("Data loaded successfully")
            #close connection
            engine.dispose()
        except Exception as e:
            self.log.error(f"Error loading data: {e}")
            raise

    def drop(self):
        """This method is used to drop the table in the db"""
        engine = self.connection()
        
        try:
            #Drop the table in the db
            with engine.connect() as conn:
                conn.execute("DELETE FROM  house_DataLake")
                self.log.info("Table dropped successfully")
        except Exception as e:
            self.log.error(f"Error dropping table: {e}")
            raise
    
    def execute(self,context):
         
        """This method is used to transform the data from the db and the save in a datawarehouse"""

        engine = self.connection() 

        inspector = inspect(engine)
        df = pd.read_sql_table('house_DataLake', con=engine)
        
        #Get inecesay columns that have more than 80% of ZEROS or NULLS
        Drop_columns = self.columnas_ceros(df)
        Drop_columns.extend(self.columnas_nulos(df))

        #Drop the columns
        df.drop(columns=Drop_columns, inplace=True)
        
        #Create a new df eith onlu numeric columns
        df_numeric = df.select_dtypes(include=['int64', 'float64'])

        #Encoded the categorical columns
        df_categorical = self.encoding(df)

        #Union the numeric and categorical columns
        df_transformed = pd.concat([df_numeric, df_categorical], axis=1)

        #Delte data from the db datalake
        self.drop()

        #Load the data into the db datawarehouse

        self.load(df_transformed)

        print("Data transformed and loaded successfully")






    #Get the columns that have more than 80% of ZEROS
    def columnas_ceros(self,dataframe):

        train_columns = dataframe.columns

        columnas = [col for col in train_columns if (dataframe[col]==0).sum() > 650 ]

        return columnas
    
    #Get the columns that have more than 80% of NULLS
    def columnas_nulos(self,dataframe):

        train_columns = dataframe.columns

        columnas = [col for col in train_columns if dataframe[col].isna().sum() > 650 ]

        return columnas
    
    def encoding(self,df):
        """This method is used to encode the categorical columns"""


        #Function to apply K-Fold target Encoding to a categorical column
        def kfold_target_encoding (df,column , target,kf):
            encoded_column = np.zeros(len(df))

            for train_idx , val_idx in kf.split(df):
                train_data , val_data = df.iloc[train_idx],df.iloc[val_idx]


                #Calcula la media de la variable objetivo por categoria en el conjunto de entrenamiento

                target_means = train_data.groupby(column)[target].mean()

                # Asignar la media al conjunto de validación
                encoded_column[val_idx] = val_data[column].map(target_means)
            
            return encoded_column
        
        #Function to apply Ordinal Encoding 

        def ordinal_encoding(df):

            #list of coliumns to encode
            lista_OrEncoding = ["LotShape", "LandSlope", "ExterQual", "ExterCond", "BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1", "BsmtFinType2", "HeatingQC", "KitchenQual", "GarageFinish", "GarageQual", "GarageCond", ]

            #Create an instance of OrdinalEncoder
            encoder = OrdinalEncoder()

            #Make a copy with the columns to encode
            df_encoded = df[lista_OrEncoding].copy()

            #Apply Ordinal Encoding to the categorical columns
            df_encoded[lista_OrEncoding] = encoder.fit_transform(df_encoded[lista_OrEncoding]) 

            return df_encoded

        #Get the categorical columns
        categorical_columns = df.select_dtypes(include=['object'])

        #Agregate 'SalesPrice' column to the categorical columns
        categorical_columns['SalesPrice'] = df['SalePrice']
        
        #List of columns that will use K-fold Target Encoding
        lista_tarEncoding = ["MSZoning", "Utilities", "Neighborhood", "Condition1", "Condition2", "BldgType", "HouseStyle", "RoofStyle", "RoofMatl", "Exterior1st", "Exterior2nd",  "Foundation", "BsmtFinType1", "Heating", "Electrical", "Functional", "GarageType", "SaleType", "SaleCondition"]

        #k-fold Target Encoding
        n_splits = 3
        kf = KFold(n_splits=n_splits,shuffle=True,random_state=42)

        #Create a new df to store the encoded columns
        df_encoded = categorical_columns[lista_tarEncoding].copy()
        df_encoded['SalesPrice'] = categorical_columns['SalesPrice']

        #Apply K-Fold Target Encoding to the categorical columns
        for column in lista_tarEncoding:
            encoded_col_name = f"{column}_encoded"
            df_encoded[encoded_col_name] = kfold_target_encoding(categorical_columns, column, 'SalesPrice', kf)

        
        #Drop the original categorical columns
        df_encoded.drop(columns=lista_tarEncoding, inplace=True)

        #Rename the encoded columns

        df_encoded.columns = [col.replace('_encoded', '') for col in df_encoded.columns]

        #Get the columns that were encodeed
        df_Ordinal_encoded =  ordinal_encoding(categorical_columns)

        #Concat df_encoded and df_Ordinal_encoded

        df_Categorical = pd.concat([df_encoded, df_Ordinal_encoded], axis=1)

        return df_Categorical







        





