# End-to-End Student Exam Performance Prediction System

![AWS Elastic Beanstalk](https://img.shields.io/badge/Deployment-AWS_Elastic_Beanstalk-orange)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-blue)
![ML Pipeline](https://img.shields.io/badge/Pipeline-Scikit_Learn-lightgrey)

## 📌 About
A production-grade machine learning system predicting student math scores based on demographic and academic factors. Features automated pipelines, cloud deployment, and modular components following MLOps best practices.

**Key Features**:
- AWS Elastic Beanstalk deployment with custom configurations
- GitHub Actions CI/CD workflow
- Modular data ingestion/transformation pipelines
- Model versioning with pickle serialization

---

## 📂 Repository Structure
```bash
End-to-End-Data-Science-Student-Exam-Performance-Prediction/
├── .elasbean_extensions/   # AWS EB configurations
│   └── python.config       # Runtime settings
├── .github/workflows/      # CI/CD pipelines
│   └── main_studentperformance3.yml
├── artifacts/              # Processed data and models
│   ├── model.pkl           # Trained model
│   └── preprocessor.pkl    # Feature engineering pipeline
├── notebook/               # Exploratory analysis
│   └── EDA_STUDENT_PERFORMANCE.ipynb
├── src/                    # Core ML logic
│   ├── components/         # Pipeline stages
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   └── pipeline/           # Training/prediction workflows
├── templates/              # Flask web interface
│   ├── home.html           # Prediction form
│   └── index.html          # Results display
├── app.py                  # Flask entry point
└── requirements.txt        # Dependency specification

🔍 Problem Statement

Analyze how student characteristics impact exam scores:
1. Input Features: Gender, Ethnicity, Parental Education, Lunch Type, Test Prep Status.
2. Target: Math Score Prediction.
3. Business Value: Early identification of at-risk students for targeted interventions.

🛠️ Project Lifecycle

Data Ingestion (src/components/data_ingestion.py)
Automated data splitting (train/test)
CSV to Pandas DataFrame conversion
Data Transformation (src/components/data_transformation.py)
Custom preprocessing pipeline
Handling categorical/numerical features
Persistent pipeline storage (artifacts/preprocessor.pkl)
Model Training (src/components/model_trainer.py)
Hyperparameter tuning
Model serialization (artifacts/model.pkl)
Performance logging
Prediction Pipeline (src/pipeline/predict_pipeline.py)
Feature validation
Preprocessing application
Model inference
Deployment (.elasbean_extensions/python.config)
Flask REST API (app.py)
AWS EB configuration
CI/CD via GitHub Actions

🚀 Installation
# Clone repository
git clone https://github.com/Kadri-Wadie/End-to-End-Data-Science-Student-Exam-Performance-Prediction

# Install dependencies
pip install -r requirements.txt

# Install as package (for local development)
pip install -e .

💻 Usage
Web Interface:
flask run --host=0.0.0.0 --port=5000
Access the prediction form at http://localhost:5000

🏗️ Deployment Architecture
CI/CD Pipeline (.github/workflows/main_studentperformance3.yml)
Automated testing
AWS EB deployment triggers
Dependency caching
AWS Elastic Beanstalk (.elasbean_extensions)
Python 3.9 runtime
WSGI configuration
Environment variables management
Monitoring (logs/)
Application logging
Error tracking
Performance metrics

📜 License
MIT License 

