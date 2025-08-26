import pandas as pd
import yaml
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.utils import ensure_dirs

params = yaml.safe_load(open("params.yaml"))
TEST_SIZE = params["data"]["test_size"]
RS = params["data"]["random_state"]

if __name__ == "__main__":
    df = pd.read_csv("data/raw/iris.csv")
    train, test = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RS,
        stratify=df["target"],
    )
    ensure_dirs("data/processed")
    train.to_csv("data/processed/train.csv", index=False)
    test.to_csv("data/processed/test.csv", index=False)