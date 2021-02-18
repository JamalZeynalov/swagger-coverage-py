import json
import re
from typing import List

import requests
from faker import Faker

from swagger_coverage_py.config import AdapterConfig


class URI:
    def __init__(self, host: str, unformatted_path: str, **uri_params):
        self.host = host
        self.formatted = unformatted_path.format(**uri_params)
        self.full = f"{self.host}{self.formatted}"
        self.raw = unformatted_path
        self.uri_params: dict = uri_params


class CoverageListener:
    def __init__(
        self, method: str, base_url: str, raw_path: str, uri_params: dict, **kwargs
    ):
        self.uri = URI(base_url, raw_path, **uri_params)
        self.other_request_params = kwargs
        self.response = requests.request(method, self.uri.full, **kwargs)
        self.method = method
        self.write_schema()

    def __host(self):
        return self.uri.host

    def __schema(self) -> List[str]:
        return [re.match(r"(^\w*):", self.uri.host).group(1)]

    def __consumes(self) -> list:
        return [self.response.request.headers.get("content-type")]

    def __produces(self) -> list:
        return [self.response.headers.get("content-type")]

    def __path_params(self) -> list:
        params_ = []
        for key, value in self.uri.uri_params.items():
            params_.append(
                {"name": key, "in": "path", "required": False, "x-example": value}
            )
        return params_

    def __query_params(self) -> list:
        if not (q_params := self.other_request_params.get("params")):
            return []

        params_ = []
        for key, value in q_params.items():
            params_.append(
                {"name": key, "in": "query", "required": False, "x-example": value}
            )
        return params_

    def __paths(self):
        dict_ = {
            self.uri.raw: {
                self.method: {
                    "parameters": self.__path_params() + self.__query_params(),
                    "responses": {self.response.status_code: {}},
                }
            }
        }
        return dict_

    def write_schema(self):
        schema_dict = {
            "swagger": "2.0",
            "host": self.__host(),
            "schemes": self.__schema(),
            "consumes": self.__consumes(),
            "produces": self.__produces(),
            "paths": self.__paths(),
        }
        rnd = Faker().pystr(min_chars=5, max_chars=5)
        file_name = (
            f"{self.method.upper()} {self.uri.formatted[1::]} ({rnd}).json".replace(
                "/", "-"
            )
        )
        with open(f"{AdapterConfig().output_dir}/{file_name}", "w+") as file:
            file.write(json.dumps(schema_dict, indent=4))

        return schema_dict
