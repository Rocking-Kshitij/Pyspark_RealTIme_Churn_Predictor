import argparse
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import s3fs
import io
import os
from decouple import Config, RepositoryEnv


# Argument parsing --- for local data--------working
# parser = argparse.ArgumentParser()
# # parser.add_argument('--data-path', type=str, default='/opt/ml/input/data/train')
# parser.add_argument('--data-path', type=str, default='s3_bucket_data')
# args = parser.parse_args()

# print("Loading data")
# # Load data
# df = pd.read_parquet(args.data_path)


#---for s3 data
env_path = os.path.join(os.path.dirname(__file__), '.env')
config = Config(RepositoryEnv(env_path))
fs = s3fs.S3FileSystem(
    key=config('s3_access_key'),
    secret=config('s3_secret_key')
)

bucket = 'mlops-clean-data-bucket'
prefix = 'customer_features'

df = pd.read_parquet(f's3://{bucket}/{prefix}/', engine='pyarrow')
#--------------

print(df.head())

df = df.dropna()
int_cols = df.select_dtypes(include=['int64']).columns
df[int_cols] = df[int_cols].astype('float64')
# print(sum(df['avg_amount'])/ len(df['avg_amount'])) # average spent
print("Loading data")
# Features + Target
x = df.drop(['customer_id', 'window', 'avg_amount'], axis=1)
y = (df['avg_amount'] > 1000).astype(int)  # is amount spent by user > 1000/ high spend usser
# Split
print(x,y)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Enable MLflow autologging
# mlflow.set_tracking_uri("http://3.235.136.64:5000") # if using external mlflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("CustomerModelExperiment")
mlflow.sklearn.autolog()
model_properties = {
    "n_estimators":200
}
with mlflow.start_run():
    # Train model
    model = RandomForestClassifier(n_estimators=model_properties["n_estimators"], class_weight='balanced')
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # Log metrics
    mlflow.log_param("n_estimators", model_properties["n_estimators"])
    mlflow.log_metric("accuracy", acc)
    print("Accuracy:", acc)
    print(classification_report(y_test, preds, zero_division=0))

    # Save model as joblib
    joblib.dump(model, "model.joblib")
    mlflow.log_artifact("model.joblib")

    # Also log model in MLflow native format (pickle)
    mlflow.sklearn.log_model(model, "random_forest_model")

    # Show artifact path
    run = mlflow.active_run()
    artifact_uri = run.info.artifact_uri
    print("Artifact URI:", artifact_uri)
