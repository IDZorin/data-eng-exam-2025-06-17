from google.cloud import storage
import logging
from .config import RESULTS_DIR, GCS_BUCKET, GCS_PREFIX, GCP_PROJECT
from .logger_setup import init

log = init(__name__)

def run() -> None:
    if not GCS_BUCKET:
        log.warning("GCS_BUCKET undefiend, skipping upload")
        return

    client = storage.Client(project=GCP_PROJECT)
    bucket = client.bucket(GCS_BUCKET)

    for path in RESULTS_DIR.glob("*"):
        blob = bucket.blob(f"{GCS_PREFIX}{path.name}")
        blob.upload_from_filename(str(path))
        log.info("Uploaded %s: gs://%s/%s", path.name, GCS_BUCKET, blob.name)

if __name__ == "__main__":
    run()