import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import List

import requests

from swagger_coverage_py.configs import API_DOCS_FORMAT, DEBUG_MODE
from swagger_coverage_py.docs_writers.api_doc_writer import write_api_doc_to_file


class CoverageReporter:
    def __init__(self, api_name: str, host: str, verify: bool = True):
        self.host = host
        self.verify = verify
        self.swagger_doc_file = f"swagger-doc-{api_name}.{API_DOCS_FORMAT}"
        self.output_dir = self.__get_output_dir()
        self.swagger_coverage_config = f"swagger-coverage-config-{api_name}.json"
        self.ignored_paths = self.__get_ignored_paths_from_config()

    def __get_output_dir(self):
        output_dir = "swagger-coverage-output"
        subdir = re.match(r"(^\w*)://(.*)", self.host).group(2).replace(".", "_").replace(":", "_")
        return f"{output_dir}/{subdir}"

    def __get_ignored_paths_from_config(self) -> List[str]:
        """Reads the swagger-coverage-config-<api_name>.json file and returns
        a list of endpoints/paths to exclude from the report

        """
        paths_to_ignore = []
        if not self.swagger_coverage_config:
            return paths_to_ignore

        with open(self.swagger_coverage_config, "r") as file:
            data = json.load(file)
            paths = data.get("rules").get("paths", {})
            if paths.get("enable", False):
                paths_to_ignore = paths.get("ignore")

        return paths_to_ignore

    def setup(
        self, path_to_swagger_json: str, auth: object = None, cookies: dict = None
    ):
        """Setup all required attributes to generate report

        :param path_to_swagger_json: The relative URL path to the swagger.json (example: "/docs/api")
        :param auth: Authentication object acceptable by "requests" library
        :param cookies: Cookies dictionary. (Usage example: set this to bypass Okta auth locally)

        """
        link_to_swagger_json = f"{self.host}{path_to_swagger_json}"

        response = requests.get(
            link_to_swagger_json, auth=auth, cookies=cookies, verify=self.verify
        )
        assert response.ok, (
            f"Swagger doc is not pulled. See details: "
            f"{response.status_code} {response.request.url}"
            f"{response.content}\n{response.content}"
        )
        if self.swagger_coverage_config:
            write_api_doc_to_file(
                self.swagger_doc_file,
                api_doc_data=response,
                paths_to_delete=self.ignored_paths,
            )

    def generate_report(self):
        base_dir = os.path.join(os.path.dirname(__file__), "swagger-coverage-commandline")
        lib_path = os.path.join(base_dir, "lib", "*")

        classpath = lib_path.replace("/", os.sep)
        command = [
            "java",
            "-cp", classpath,
            "com.github.viclovsky.swagger.coverage.CommandLine",
            "-s", self.swagger_doc_file,
            "-i", self.output_dir,
        ]
        if self.swagger_coverage_config:
            command.extend(["-c", self.swagger_coverage_config])

        if not DEBUG_MODE:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        else:
            subprocess.run(command, check=True)

    def cleanup_input_files(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
