from environs import Env

import rootpath
from dotenv import load_dotenv

load_dotenv(f"{rootpath.detect()}/.env")
env = Env()

API_DOCS_TYPE = env.str("API_DOCS_TYPE", default="openapi")  # "swagger"
API_DOCS_VERSION = env.str("API_DOCS_VERSION", default="3.0.0")  # "2.0"
API_DOCS_FORMAT = env.str("API_DOCS_FORMAT", default="json")  # "yaml"
IS_DISABLED = env.bool("API_COVERAGE_REPORTS_DISABLED", default=False)  # If True then requests won't be recorded
