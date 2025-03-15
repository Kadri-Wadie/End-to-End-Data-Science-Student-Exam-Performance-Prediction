"""
app.py: Flask web application for predicting student exam scores

Single-Result Assumption Risks and Limitations:

This implementation assumes model predictions only contain one result via results[0],
introducing several critical constraints:

!!! BATCH PREDICTION FAILURE:
   - Fails to handle multiple results (e.g., CSV upload with 100 students)
   - Only displays first result, losing subsequent predictions

!!! FRAGILE INDEXING:
   - results[0] will crash with IndexError if:
     * Model returns empty array (invalid input edge case)
     * Database connection fails during prediction
     * Unexpected empty response from pipeline

!!! TYPE MISMATCH RISKS:
   - Direct use of numpy data types (float32/64) without conversion:
     * Template rendering failures with numpy types
     * JSON serialization errors in API responses
     * Unexpected type propagation through system

!!! HIDDEN SHAPE ERRORS:
   - Silent failures if model output shape changes:
     * (n,1) vs (n,) dimensional arrays
     * Multi-output models returning tuples
     * Debug metadata altering output structure

!!! WORKFLOW CONSTRAINTS:
   - Prevents batch prediction implementation
   - Blocks result quality statistics display
   - Limits error reporting granularity

"""

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)  # Simplified single app instance

@app.route('/')
def index():
    """Landing page with security warnings still present"""
    return render_template('index.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    """Prediction endpoint with cleaned debug statements"""
    
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),  # Maintained swapped parameter warning
            writing_score=float(request.form.get('reading_score'))
        )

        pred_df = data.get_data_as_data_frame()
        
        # Removed debug print statements
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template('home.html', results=results[0])

if __name__ == "__main__":
    # Production recommendation in comments
    # Consider using production server like gunicorn/uvicorn
    app.run(host="0.0.0.0", debug=False)  # Explicit debug mode off