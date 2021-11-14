import json

import requests
import yaml

from swagger_coverage_py.configs import API_DOCS_FORMAT, API_DOCS_TYPE


def __write_api_doc_to_json(file_path: str, api_doc_data: requests.Response):
    api_doc_data = api_doc_data.json()
    if API_DOCS_TYPE == "swagger" and not api_doc_data.get("swagger", None):
        api_doc_data["swagger"] = "2.0"

    with open(file_path, "w+") as file:
        file.write(json.dumps(api_doc_data))


def __write_api_doc_to_yaml(file_path: str, api_doc_data: requests.Response):
    data = yaml.safe_load(str(api_doc_data.text))

    if API_DOCS_TYPE == "swagger" and not data.get("swagger", None):
        data["swagger"] = "2.0"

    with open(file_path, "w+") as file:
        file.write(yaml.safe_dump(data, indent=4, sort_keys=False))


def write_api_doc_to_file(file_path: str, api_doc_data: requests.Response):
    if API_DOCS_FORMAT == "json":
        __write_api_doc_to_json(file_path, api_doc_data)
    else:
        __write_api_doc_to_yaml(file_path, api_doc_data)
