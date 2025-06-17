import json, joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from .config import BASE_DIR
from .logger_setup import init

log = init(__name__)

def run(model_path: str) -> str:
    bundle = joblib.load(model_path)
    model, X_test, y_test = bundle["model"], bundle["X_test"], bundle["y_test"]
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
    }
    metrics_path = BASE_DIR / "results" / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    return str(metrics_path)

if __name__ == "__main__":
    import sys; log.info(run(sys.argv[1]))
