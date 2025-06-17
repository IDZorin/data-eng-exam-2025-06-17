import pandas as pd
from sklearn.preprocessing import StandardScaler
from .config import TARGET_COLUMN, BASE_DIR
from .logger_setup import init

log = init(__name__)

def run(input_path: str) -> str:
    df = pd.read_csv(input_path)
    df.columns = (["id", "diagnosis"] +
                  [f"feature_{i+1}" for i in range(1, df.shape[1]-1)])
    X = df.drop(columns=["id", TARGET_COLUMN])
    y = df[TARGET_COLUMN].map({"M": 1, "B": 0})
    X_scaled = StandardScaler().fit_transform(X)
    out = pd.DataFrame(X_scaled, columns=X.columns)
    out[TARGET_COLUMN] = y
    prep_path = BASE_DIR / "results" / "data_prepared.csv"
    out.to_csv(prep_path, index=False)
    return str(prep_path)

if __name__ == "__main__":
    import sys;  log.info(run(sys.argv[1]))
