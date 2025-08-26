import yaml, joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.sklearn

params = yaml.safe_load(open("params.yaml"))
TARGET = params["training"]["target"]
EXP_NAME = params["training"]["experiment_name"]

mlflow.set_experiment(EXP_NAME)
mlflow.sklearn.autolog(log_models=True)

if __name__ == "__main__":
    train = pd.read_csv("data/processed/train.csv")
    X = train.drop(columns=[TARGET])
    y = train[TARGET]

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(
            n_estimators=params["model"]["n_estimators"],
            max_depth=params["model"]["max_depth"],
            random_state=params["model"]["random_state"],
        )),
    ])

    with mlflow.start_run() as run:
        model.fit(X, y)
        Path("models").mkdir(parents=True, exist_ok=True)
        joblib.dump(model, "models/model.pkl")
        # El artefacto MLflow del modelo queda en runs:/<run_id>/model por autolog
        print(f"Run ID: {run.info.run_id}")