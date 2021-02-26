import json
import os
import platform
import re
from typing import List

import requests
from faker import Faker


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
        """Records an HTTP request as a file in swagger format

        :param method: the HTTP method name in lowercase.
        :param base_url: Base URl with a protocol but without a path. (e.g. "https://petstore.swagger.io")
        :param raw_path: Not formatted URL path.
            Parameters names in braces will be used for further formatting  (e.g. "/v2/store/order/{orderId}")
        :param uri_params: URL path parameters. Must match to parameters names specified in "raw_path"
        :param kwargs: Optional arguments that are applicable
            for appropriate request of "requests" library. (e.g. "auth", "headers", "cookies", etc.)
        """
        self.__uri = URI(base_url, raw_path, **uri_params)
        self.__other_request_params = kwargs

        self.response = requests.request(method, self.__uri.full, **kwargs)

        self.__method = method
        self.__write_schema()

    def __host(self):
        return self.__uri.host

    def __schema(self) -> List[str]:
        return [re.match(r"(^\w*):", self.__uri.host).group(1)]

    def __consumes(self) -> list:
        return [self.response.request.headers.get("content-type")]

    def __produces(self) -> list:
        return [self.response.headers.get("content-type")]

    def __path_params(self) -> list:
        params_ = []
        for key, value in self.__uri.uri_params.items():
            params_.append(
                {"name": key, "in": "path", "required": False, "x-example": value}
            )
        return params_

    def __query_params(self) -> list:
        if not (q_params := self.__other_request_params.get("params")):
            return []

        params_ = []
        for key, value in q_params.items():
            params_.append(
                {"name": key, "in": "query", "required": False, "x-example": value}
            )
        return params_

    def __paths(self):
        dict_ = {
            self.__uri.raw: {
                self.__method: {
                    "parameters": self.__path_params() + self.__query_params(),
                    "responses": {self.response.status_code: {}},
                }
            }
        }
        return dict_

    def __output_subdir(self):
        return re.match(r"(^\w*)://(.*)", self.__uri.host).group(2)

    def __write_schema(self):
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
            f"{self.__method.upper()} {self.__uri.formatted[1::]} ({rnd}).json".replace(
                "/", "-"
            ).replace(":", "_")
        )
        path_ = f"swagger-coverage-output/{self.__output_subdir()}"
        file_path = f"{path_}/{file_name}"

        try:
            with open(file_path, "w+") as file:
                file.write(json.dumps(schema_dict, indent=4))

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
