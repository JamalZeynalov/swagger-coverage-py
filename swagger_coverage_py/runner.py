import glob
import json
import os
import shutil
from pathlib import Path

import requests
from swagger_coverage_py.config import AdapterConfig


class Runner:
    def __init__(self, api_name: str):
        self.config = AdapterConfig(api_name)
        self.swagger_doc_file = f"swagger-{api_name}.json"

    def setup(self, link_to_swagger_json: str, auth: object = None):
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)

        response = requests.get(link_to_swagger_json, auth=auth)
        assert response.ok, f"Swagger doc is not pulled. See details: " \
                            f"{response.status_code} {response.request.url}" \
                            f"{response.content}\n{response.content}"
        swagger_json_data = response.json()

        with open(self.swagger_doc_file, "w+") as f:
            swagger_json_data["swagger"] = "2.0"
            f.write(json.dumps(swagger_json_data))

    def generate_report(self):
        for mask in self.config.ignore_requests:
            files_list = glob.glob(f"{self.config.output_dir}/{mask}", recursive=True)
            for file_path in files_list:
                try:
                    os.remove(file_path)
                except OSError:
                    print(f"Error while deleting file: {file_path}")

        cmd_ = "src/swagger-coverage/swagger_coverage_py/swagger-coverage-commandline/bin/swagger-coverage-commandline"
        if config := self.config.swagger_coverage_config:
            os.system(f"{cmd_} -s {self.swagger_doc_file} -i {self.config.output_dir} -c {config}")
        else:
            os.system(f"{cmd_} -s {self.swagger_doc_file} -i {self.config.output_dir}")

    def cleanup_input_files(self):
        shutil.rmtree(self.config.output_dir, ignore_errors=True)
