from mlflow.tracking import MlflowClient

client = MlflowClient(tracking_uri="http://localhost:5000")

# Get latest run ID
experiment = client.get_experiment_by_name("CustomerModelExperiment")
runs = client.search_runs(experiment.experiment_id, order_by=["start_time desc"])
run_id = runs[0].info.run_id

# Register the model
model_uri = f"runs:/{run_id}/model"
model_name = "HighSpenderClassifier"

client.create_registered_model(model_name)
client.create_model_version(name=model_name, source=model_uri, run_id=run_id)
