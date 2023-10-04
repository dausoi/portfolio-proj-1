"""
1. Download xml file locally
2. Download pages from the xml file, only relevant to the html scraping
3. Upload to the data lake (i.e. Google Cloud Storage)
"""

from pathlib import Path
from datetime import datetime
import requests