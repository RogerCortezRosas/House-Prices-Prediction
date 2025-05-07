from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import tempfile
import os
from typing import List
from Modelprediction import model  # Asegúrate de que 'model' siga una interfaz clara
import logging # Allows to log errors and information
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title ="House Price Prediction API",
    description = "API for predicting house prices from a CSV file",
    version = "1.0.0",
)


@app.post("/predict",summary="Predict house prices from a CSV file")
async def predict(file: UploadFile = File(...)):
   
    """Endpoint to predict house prices from a CSV file."""

    # Check if the uploaded file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            shutil.copyfileobj(file.file, tmp) # This is useful to not load the entire file into memory
            temp_file_path = tmp.name

        # Read the file into a DataFrame (assuming it's a CSV file)
        df = pd.read_csv(temp_file_path)

        # Validate the dataframe is not empty 
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV is empty")

        # Create an instance of the model class and make a prediction
        model_instance = model(df)
        prediction = model_instance.Prediction()

        # Clean up the temporary file
        os.remove(temp_file_path)

        return JSONResponse(content={"prediction": prediction})
    
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing CSV file")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))