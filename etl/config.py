from pathlib import Path
import os
from dotenv import load_dotenv
from .logger_setup import init

log = init(__name__)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]

# data download URL
DATA_URL = ("https://archive.ics.uci.edu/ml/"
            "machine-learning-databases/"
            "breast-cancer-wisconsin/wdbc.data")

RANDOM_STATE   = 42
TARGET_COLUMN  = "diagnosis"

# results directory
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# google cloud storage
GCP_PROJECT   = os.getenv("GCP_PROJECT")
GCS_BUCKET    = os.getenv("GCS_BUCKET")
GCS_PREFIX    = os.getenv("GCS_PREFIX", "breast_cancer/")

# workaround for docker and local make to read json keys
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
cred_path = Path(cred_path)
if not cred_path.is_absolute():
    cred_path = (BASE_DIR / cred_path).resolve()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_path)