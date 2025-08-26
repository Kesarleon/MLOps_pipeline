import json
import yaml
import joblib
import pandas as pd
import mlflow
from sklearn.metrics import accuracy_score, f1_score

params = yaml.safe_load(open("params.yaml"))
TARGET = params["training"]["target"]
EXPERIMENT_NAME = params["training"]["experiment_name"]

if __name__ == "__main__":
    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run():
        test = pd.read_csv("data/processed/test.csv")
        X = test.drop(columns=[TARGET])
        y = test[TARGET]
        model = joblib.load("models/model.pkl")

        pred = model.predict(X)
        metrics = {
            "accuracy": float(accuracy_score(y, pred)),
            "f1_macro": float(f1_score(y, pred, average="macro")),
        }
        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        print(metrics)
        mlflow.log_metrics(metrics)
