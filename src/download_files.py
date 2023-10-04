"""
PREREQUISITE:
pip install google-cloud-storage
export GOOGLE_APPLICATION_CREDENTIALS=<YOUR CREDENTIAL FILE>

1. Download xml file locally
2. Upload all the files to the data lake (i.e. Google Cloud Storage)
"""

from pathlib import Path
from urllib import parse
from datetime import datetime
import requests
import os
import typing
from google.cloud import storage

def _get_filename(url: str) -> str:
    """ Construct a new filename from url path, with timestamp at the end """
    parsed = parse.urlparse(url)
    sitename = parsed.netloc
    sitename = sitename.replace(".", "")
    p, e = os.path.splitext(parsed.path)
    p = p.replace("/", "")
    filename = sitename + p + f"_{datetime.strftime(datetime.now(), '%Y-%m-%d_%H%M%S')}" + e
    return filename

def save_local(url: str, save_dir: Path) -> Path:
    """ Download a file locally, returns local path to the downloaded file """
    h = {"user-agent": "my-user-agent"}  # Bookscape doesn't allow No-user-agent requests
    r = requests.get(url, headers=h)
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = Path(os.path.join(save_dir, Path(_get_filename(url))))
    f = open(save_path, "wb")
    f.write(r.content)
    f.close()
    return save_path

def upload_to_gcs(gcs_path: typing.Union[str, Path], local_path: Path, bucket_name: str):
    """ Upload a file to Google Cloud Storage """
    gcs_path = str(gcs_path) if isinstance(gcs_path, Path) else gcs_path
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)

if __name__ == "__main__":
    download_url = f"https://bookscape.co/sitemap.xml"
    save_dir = Path("bookscape")
    filename = save_local(download_url, save_dir)
    # upload_to_gcs(gcs_path=filename, local_path=filename, bucket_name="de-zoomcamp-dtl-test")