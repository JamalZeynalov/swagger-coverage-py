from requests import Response

from swagger_coverage_py.configs import API_DOCS_TYPE, API_DOCS_VERSION
from swagger_coverage_py.results_writers.base_schemas_manager import ApiDocsManagerBase
from swagger_coverage_py.uri import URI


class OpenApiSchemasManager(ApiDocsManagerBase):
    def __init__(self, uri: URI, method: str, response: Response, kwargs: dict):
        super().__init__(uri, response, kwargs, method)

    def _paths(self):
        path_ = self._uri.raw.split("?")[0]
        dict_ = {
            path_: {
                self._method: {
                    "parameters": self._get_path_params() + self._get_query_params(),
                    "responses": {self._response.status_code: {}},
                }
            }
        }

        body_params = self._get_body_params()
        if body_params:
            dict_[path_][self._method]["requestBody"] = body_params
        return dict_

    def _get_schema(self):
        schema_dict = {
            API_DOCS_TYPE: API_DOCS_VERSION,
            "info": {"title": "Recorded Request"},
            "paths": self._paths(),
        }
        return schema_dict
