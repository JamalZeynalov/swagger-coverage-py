import json

import rootpath
from singleton_decorator import singleton


@singleton
class ListenerConfig:
    def __init__(
        self,
    ):
        root = rootpath.detect()

        with open(f"{root}/swagger-coverage-adapter-config.json", "r") as f:
            json_config: dict = json.loads(f.read())

        self.output_dir = json_config.get("output_dir")
        self.swagger_coverage_config = json_config.get("swagger_coverage_config")
        self.link_to_swagger_json = json_config.get("link_to_swagger_json")

        ignore = json_config.get("ignore_requests")
        self.ignore_requests = ignore if ignore else []
