import requests

from swagger_coverage_py.request_schema_handler import RequestSchemaHandler


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
        self.response = requests.request(method, self.__uri.full, **kwargs)

        RequestSchemaHandler(self.__uri, method, self.response, kwargs).write_schema()
