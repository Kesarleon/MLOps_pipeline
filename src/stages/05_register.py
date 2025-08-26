"""
Registra el último run como versión de modelo en MLflow Model Registry.
Requiere que MLFLOW_TRACKING_URI esté configurado (archivo local o servidor).
"""
import yaml
import mlflow
from mlflow.tracking import MlflowClient

params = yaml.safe_load(open("params.yaml"))
EXP_NAME = params["training"]["experiment_name"]
MODEL_NAME = params["training"]["registered_model_name"]

if __name__ == "__main__":
    exp = mlflow.get_experiment_by_name(EXP_NAME)
    if exp is None:
        raise RuntimeError(f"Experimento no encontrado: {EXP_NAME}")
    client = MlflowClient()
    runs = client.search_runs(exp.experiment_id, order_by=["attributes.start_time DESC"], max_results=1)
    if not runs:
        raise RuntimeError("No hay runs para registrar")
    run = runs
