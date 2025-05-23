import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sklearn.preprocessing import RobustScaler , OrdinalEncoder
import joblib
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    filename='model_prediction.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s' )
logger = logging.getLogger(__name__)

class model():

    def __init__(self,df):
        self.df = df
        pass

    def Prediction(self):
        """This method is use to predict the house price using the Random Forest Regressor model.Charge the model previously trained"""
        try:
            #Load the model
            model = joblib.load('model.pkl')

            # Transform tht data using Transform function
            df_transformed = self.Transform()

            df_transformed.fillna(0, inplace=True)

            
            #Make a prediction
            prediction = model.predict(df_transformed)

            result  = int(prediction[0])

            return result

        except Exception as e:
            logger.exception(f"Error during prediction: {e}")
           
            raise Exception(" The prediction could not be completed.Try again later")

        
    def Transform(self):
        """This method is used to transform the data"""

       
        try:

            #fill the missing values with zero
            self.df.fillna(0, inplace=True)

            #filter the columns that are not needed for the prediction
            engine = self.connection()
            df_WH = pd.read_sql_table('house_WareHouse', engine)
            columns_to_drop = self.df.columns.difference(df_WH.columns) #Get the columns that are not in the DataWarehouse
            
            self.df.drop(columns=columns_to_drop, inplace=True)
            self.df.drop(columns=['Id'], inplace=True) #Drop the Id column


            #Separate numerical columns
            df_numeric = self.df.select_dtypes(include=['int64', 'float64'])

            # Encode categorical columns
            df_categorical = self.encoding()

            #concat the numerical and categorical columns
            df_transformed = pd.concat([df_numeric, df_categorical], axis=1)

            #Scale the data using RobustScaler
            df_scaled = self.robustScaler(df_transformed)

            return df_scaled

        except Exception as e:
            logger.exception(f"Error during transformation: {e}")
            raise Exception("Error during transformation")

        




    def robustScaler(self,dataframe):
        """This method scales the data using RobustScaler and helps to reduce the influence of outliers"""

        try:
            #Check if the dataframe is empty
            if dataframe.empty:
                raise ValueError("The dataframe is empty.")

            #Check if the dataframe has only one column
            if len(dataframe.columns) == 1:
                raise ValueError("The dataframe has only one column.")
            Robustscaler = RobustScaler()
            Numeric_scaled = Robustscaler.fit_transform(dataframe)
            dataScaled = pd.DataFrame(Numeric_scaled,columns=dataframe.columns)

            return dataScaled
        
        except Exception as e:
            logger.exception(f"Error in robustScaler method: {e}")
            raise Exception("Scaeling error")


    def encoding(self):
        """This method is used to encode the categorical columns.One of the with the target 
        encoding and the other with ordinal encoding"""


        #Function to applytarget Encoding to a categorical column
        def kfold_target_encoding (df_WH , df_to_Predict):

            try:

                lista_tarEncoding = ["MSZoning", "Utilities", "Neighborhood", "Condition1", "Condition2", "BldgType", "HouseStyle", "RoofStyle", "RoofMatl", "Exterior1st", "Exterior2nd",  "Foundation", "BsmtFinType1", "Heating", "Electrical", "Functional", "GarageType", "SaleType", "SaleCondition"]

                df_new = df_to_Predict[lista_tarEncoding].copy()
                for columna in lista_tarEncoding:
                    # Usar el mapeo calculado en el conjunto de entrenamiento
                    category_means = df_WH.groupby(columna)['SalePrice'].mean()
                    
                    # Aplicar el encoding a los nuevos datos
                    encoded_col_name = f"{columna}_encoded"
                    
                    df_new[encoded_col_name] = df_new[columna].map(category_means)
                        #Drop the original categorical columns
                        
                df_new.drop(columns=lista_tarEncoding, inplace=True)

                #Rename the encoded columns

                df_new.columns = [col.replace('_encoded', '') for col in df_new.columns]
        
                return df_new
            except Exception as e:
                logger.exception(f"Error in kfold_target_encoding method: {e}")
                raise Exception("Error in target encoding")
            
            
        
        #Function to apply Ordinal Encoding 

        def ordinal_encoding(df):
            
            try:
                #list of coliumns to encode
                lista_OrEncoding = ["LotShape", "LandSlope", "ExterQual", "ExterCond", "BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1", "BsmtFinType2", "HeatingQC", "KitchenQual", "GarageFinish", "GarageQual", "GarageCond", ]

                #Create an instance of OrdinalEncoder
                encoder = OrdinalEncoder()

                #Make a copy with the columns to encode
                df_encoded = df[lista_OrEncoding].copy()

                #Apply Ordinal Encoding to the categorical columns
                df_encoded[lista_OrEncoding] = encoder.fit_transform(df_encoded[lista_OrEncoding]) 

                return df_encoded
            except Exception as e:
                logger.exception(f"Error in ordinal_encoding method: {e}")
                raise Exception("Error in ordinal encoding")
        

        
        try:
            #Get the categorical columns
            categorical_columns = self.df.select_dtypes(include=['object'])


            # Get de data in the DataWarehouse
            engine = self.connection()
            df_WH = pd.read_sql_table('house_WareHouse', engine)

            #Get encoded columns from function kfold_target_encoding
            df_target_encoded = kfold_target_encoding(df_WH, categorical_columns)

            #Get encoded columns from function ordinal_encoding
            df_ordinal_encoded = ordinal_encoding(categorical_columns)

            #Concat df_encoded and df_Ordinal_encoded
            df_encoded = pd.concat([df_target_encoded, df_ordinal_encoded], axis=1)

            return df_encoded
        
        except Exception as e:
            logger.exception(f"Error in encoding method: {e}")
            raise Exception(f"Error in encoding method: {e}")

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
            return engine
        
        except Exception as e:
            logger.exception(f"Error creating connection: {e}")
            
            raise Exception(f"Error creating connection: {e}")

        

