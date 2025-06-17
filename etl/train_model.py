import joblib, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from .config import TARGET_COLUMN, RANDOM_STATE, BASE_DIR
from .logger_setup import init

log = init(__name__)

def run(data_path: str) -> str:
    df = pd.read_csv(data_path)
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    model_path = BASE_DIR / "results" / "model.pkl"
    joblib.dump({"model": model, "X_test": X_test, "y_test": y_test}, model_path)
    return str(model_path)

if __name__ == "__main__":
    import sys; log.info(run(sys.argv[1]))
