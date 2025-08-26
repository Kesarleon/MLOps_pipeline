from sklearn.datasets import load_iris
import pandas as pd
from pathlib import Path
from src.utils import ensure_dirs

if __name__ == "__main__":
    X, y = load_iris(return_X_y=True, as_frame=True)
    df = X.copy()
    df["target"] = y
    ensure_dirs("data/raw")
    df.to_csv("data/raw/iris.csv", index=False)