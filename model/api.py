from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from Modelprediction import model
import io
import pandas as pd

app = FastAPI()


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = f"temp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read the file into a DataFrame (assuming it's a CSV file)
        df = pd.read_csv(temp_file_path)

        # Create an instance of the model class and make a prediction
        model_instance = model(df)
        prediction = model_instance.Prediction()

        # Clean up the temporary file
        os.remove(temp_file_path)

        return JSONResponse(content={"prediction": prediction})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))