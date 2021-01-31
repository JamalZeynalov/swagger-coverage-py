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
        shutil.rmtree({self.config.output_dir})
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)

        swagger_json_data = requests.get(self.config.link_to_swagger_json, auth=auth).json()
        with open('./swagger.json') as f:
            f.write(json.dumps(swagger_json_data))

    def collect(self):
        for mask in self.config.ignore_requests:
            glob.glob(mask, recursive=True)

        os.system(
            f"../swagger-coverage-commandline/bin/swagger-coverage-commandline "
            f"-s ./swagger.json "
            f"-i {self.config.output_dir} "
            f"-c  {self.config.swagger_coverage_config}"
        )


Runner().collect()