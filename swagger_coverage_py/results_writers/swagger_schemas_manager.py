import re
from typing import List

from requests import Response

from swagger_coverage_py.configs import API_DOCS_TYPE, API_DOCS_VERSION
from swagger_coverage_py.results_writers.base_schemas_manager import ApiDocsManagerBase
from swagger_coverage_py.uri import URI


class SwaggerSchemasManager(ApiDocsManagerBase):
    def __init__(self, uri: URI, method: str, response: Response, kwargs: dict):
        super().__init__(uri, response, kwargs, method)
        self._uri = uri
        self.__response = response

    def __host(self):
        return self._uri.host

    def __schema(self) -> List[str]:
        return [re.match(r"(^\w*):", self._uri.host).group(1)]

    def __consumes(self) -> list:
        return [self.__response.request.headers.get("content-type", "")]

    def __produces(self) -> list:
        return [self.__response.headers.get("content-type", "")]

    def _paths(self):
        path_ = self._uri.raw.split("?")[0]
        params = (
            self._get_path_params() + self._get_query_params() + self._get_body_params()
        )
        dict_ = {
            path_: {
                self._method: {
                    "parameters": params,
                    "responses": {self.__response.status_code: {}},
                }
            }
        }
        return dict_

    def _get_schema(self):
        schema_dict = {
            API_DOCS_TYPE: API_DOCS_VERSION,
            "host": self.__host(),
            "schemes": self.__schema(),
            "consumes": self.__consumes(),
            "produces": self.__produces(),
            "paths": self._paths(),
        }
        return schema_dict
