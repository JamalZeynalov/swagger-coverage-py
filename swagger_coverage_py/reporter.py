import json
import os
import re
import shutil
from pathlib import Path

import requests


class CoverageReporter:
    def __init__(self, api_name: str, host: str):
        self.host = host
        self.swagger_doc_file = f"swagger-{api_name}.json"
        self.output_dir = self.__get_output_dir()
        self.ignore_requests = []
        self.swagger_coverage_config = f"swagger-coverage-config-{api_name}.json"

    def __get_output_dir(self):
        output_dir = "swagger-coverage-output"
        subdir = re.match(r"(^\w*)://(.*)", self.host).group(2)
        return f"{output_dir}/{subdir}"

    def setup(self, path_to_swagger_json: str, auth: object = None):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        link_to_swagger_json = f"{self.host}{path_to_swagger_json}"

        response = requests.get(link_to_swagger_json, auth=auth)
        assert response.ok, (
            f"Swagger doc is not pulled. See details: "
            f"{response.status_code} {response.request.url}"
            f"{response.content}\n{response.content}"
        )
        swagger_json_data = response.json()

        with open(self.swagger_doc_file, "w+") as f:
            swagger_json_data["swagger"] = "2.0"
            f.write(json.dumps(swagger_json_data))

    def generate_report(self):
        inner_location = "swagger-coverage/swagger_coverage_py/swagger-coverage-commandline/bin/swagger-coverage-commandline"
        cmd_ = f"src/{inner_location}"
        cmd_venv = f"venv/src/{inner_location}"
        cmd_venv_2 = f".venv/src/{inner_location}"

        if Path(cmd_).exists():
            cmd_path = cmd_
        elif Path(cmd_venv).exists():
            cmd_path = cmd_venv
        elif Path(cmd_venv_2).exists():
            cmd_path = cmd_venv_2
        else:
            raise Exception(
                f"No commandline tools is found in following locations:\n{cmd_}\n{cmd_venv}\n"
            )
        if config := self.swagger_coverage_config:
            command = f"{cmd_path} -s {self.swagger_doc_file} -i {self.output_dir} -c {config}"
            os.system(command)
        else:
            os.system(f"{cmd_path} -s {self.swagger_doc_file} -i {self.output_dir}")

    def cleanup_input_files(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)
