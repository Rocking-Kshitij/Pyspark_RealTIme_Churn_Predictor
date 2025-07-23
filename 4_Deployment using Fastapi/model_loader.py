import os
import mlflow.pyfunc
#from decouple import Config, RepositoryEnv
from dotenv import load_dotenv

load_dotenv()

# if using decouple
# env_path = os.path.join(os.path.dirname(__file__), '.env')
# config = Config(RepositoryEnv(env_path))

# tracking_uri = config("MLFLOW_TRACKING_URI")
# model_name = config("MODEL_NAME")
# model_stage = config("MODEL_STAGE")

#if using .env
load_dotenv()

tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
model_name = os.getenv("MODEL_NAME")
model_alias = os.getenv("MODEL_ALIAS")


mlflow.set_tracking_uri(tracking_uri)

print(f"Loading model {model_name} from MLflow Registry...")

# Model load from Registry
model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}@{model_alias}"
)
