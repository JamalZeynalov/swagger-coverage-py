import glob
import json
import os
import shutil
from pathlib import Path

import requests

from swagger_coverage_py.config import ListenerConfig


class Runner:
    def __init__(self):
        self.config = ListenerConfig()

    def setup(self, auth: object = None):
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)

        swagger_json_data = requests.get(
            self.config.link_to_swagger_json, auth=auth
        ).json()
        with open("swagger.json", "w+") as f:
            swagger_json_data["swagger"] = "2.0"
            f.write(json.dumps(swagger_json_data))

    def collect(self):
        for mask in self.config.ignore_requests:
            files_list = glob.glob(f"{self.config.output_dir}/{mask}", recursive=True)
            for file_path in files_list:
                try:
                    os.remove(file_path)
                except OSError:
                    print(f"Error while deleting file: {file_path}")

        cmd_ = "src/swagger-coverage/swagger_coverage_py/swagger-coverage-commandline/bin/swagger-coverage-commandline"
        if config := self.config.swagger_coverage_config:
            os.system(f"{cmd_} -s swagger.json -i {self.config.output_dir} -c {config}")
        else:
            os.system(f"{cmd_} -s swagger.json -i {self.config.output_dir}")

    def cleanup_input_files(self):
        shutil.rmtree(self.config.output_dir, ignore_errors=True)
