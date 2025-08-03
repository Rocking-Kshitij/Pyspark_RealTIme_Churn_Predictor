# ChurnPredictor

This project simulates a real-world customer churn prediction system using modern data engineering and MLOps tools. It's built in modular steps — from event simulation to deployment — making it easy to extend or integrate into larger systems.

---

## Components

### 1. Kafka Stream Simulator
- **Stack:** Kafka, Python
- **What it does:** Simulates real-time user event streams using Kafka. Producers generate JSON events; consumers process them downstream.

### 2. PySpark Data Pipeline (Databricks)
- **Stack:** PySpark on Databricks
- **What it does:** Reads Kafka events, performs cleaning & feature engineering, and writes a processed feature store to S3.

### 3. Model Training with MLflow
- **Stack:** Scikit-learn, MLflow, DVC
- **What it does:** Trains a churn prediction model. All experiments, metrics, and artifacts are tracked with MLflow. Dataset versions managed using DVC.

### 4. FastAPI Model Deployment (Dockerized)
- **Stack:** FastAPI, Docker
- **What it does:** Serves the trained model through a lightweight REST API — great for local testing or integration with frontends.

---

## Getting Started

To run the full pipeline locally, you'd typically:
1. Start Kafka and simulate events.
2. Run the Spark job on Databricks, it will process and store on s3 bucket.
3. Train and track the model using `train.py`.
4. Build and run the FastAPI app via Docker.


