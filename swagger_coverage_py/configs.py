import os

import rootpath
from dotenv import load_dotenv

load_dotenv(f"{rootpath.detect()}/.env")

API_DOCS_TYPE = os.environ.get("API_DOCS_TYPE", "openapi")  # "swagger"
API_DOCS_VERSION = os.environ.get("API_DOCS_VERSION", "3.0.0")  # "2.0"
API_DOCS_FORMAT = os.environ.get("API_DOCS_FORMAT", "json")  # "yaml"
