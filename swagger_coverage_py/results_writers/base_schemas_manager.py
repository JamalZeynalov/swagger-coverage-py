import json
import os
import platform
import re

import yaml
from faker import Faker
from requests import Response

from swagger_coverage_py.configs import API_DOCS_FORMAT
from swagger_coverage_py.uri import URI


class ApiDocsManagerBase:
    def __init__(self, uri: URI, response: Response, kwargs: dict, method: str = None):
        self._uri = uri
        self._method = method
        self._response: Response = response
        self.__other_request_params = kwargs

    def _get_path_params(self) -> list:
        params_ = []
        for key, value in self._uri.uri_params.items():
            params_.append(
                {"name": key, "in": "path", "required": False, "x-example": str(value)}
            )
        return params_

    def _get_body_params(self):
        if self._response.request.body is not None:
            request_body: dict = {
                "content": {
                    "application/json": {
                        "example": json.loads(self._response.request.body)
                    }
                }
            }
        else:
            request_body = None

        return request_body

    def _get_query_params(self) -> list:
        q_params = list(self.__other_request_params.get("params", {}).items())
        raw = self._uri.raw.split("?")
        if len(raw) > 1:
            q_params += [tuple(x.split("=")) for x in str(raw[1]).split("&")]
        if not q_params:
            return []

        params_ = []
        for key, value in q_params:
            params_.append(
                {"name": key, "in": "query", "required": False, "x-example": str(value)}
            )
        return params_

    def __get_output_subdir(self):
        return re.match(r"(^\w*)://(.*)", self._uri.host).group(2)

    def write_schema(self):
        schema_dict = self._get_schema()
        rnd = Faker().pystr(min_chars=5, max_chars=5)
        file_name = f"{self._method.upper()} {self._uri.formatted[1::]}".replace(
            "/", "-"
        ).replace(":", "_")
        path_ = f"swagger-coverage-output/{self.__get_output_subdir()}"
        file_path = f"{path_}/{file_name}".split("?")[0]
        file_path = f"{file_path} ({rnd}).{API_DOCS_FORMAT}"

        try:
            with open(file_path, "w+") as file:
                if API_DOCS_FORMAT == "yaml":
                    file.write(yaml.safe_dump(schema_dict, indent=4, sort_keys=False))
                elif API_DOCS_FORMAT == "json":
                    file.write(json.dumps(schema_dict, indent=4))
                else:
                    raise Exception(
                        f"Unexpected docs format: {API_DOCS_FORMAT}. Valid formats: json, yaml"
                    )

        except FileNotFoundError as e:
            system_ = platform.system()
            abs_path = os.path.abspath(file_path)

            if system_ == "Windows" and len(abs_path) > 256:
                raise EnvironmentError(
                    f"Absolute path length is greater than 256 symbols:\n"
                    f"{abs_path}\n"
                    f"To remove this restriction you can use this guide: "
                    f"https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation#enable-long-paths-in-windows-10-version-1607-and-later "
                )
            else:
                raise Exception(
                    f"Cannot write to file.\n"
                    f"Path: {abs_path}\n"
                    f"Details: {e.strerror}"
                )

        return schema_dict
