import pandas as pd
import requests
from io import StringIO
from .config import DATA_URL, BASE_DIR
from .logger_setup import init

log = init(__name__)

def run() -> str:
    resp = requests.get(DATA_URL, timeout=30)
    resp.raise_for_status()
    df = pd.read_csv(StringIO(resp.text), header=None)
    raw_path = BASE_DIR / "results" / "raw_data.csv"
    df.to_csv(raw_path, index=False)
    return str(raw_path)

if __name__ == "__main__":
    log.info(run())
