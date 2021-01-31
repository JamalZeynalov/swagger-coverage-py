from typing import List

from singleton_decorator import singleton


@singleton
class ListenerConfig:
    def __init__(
        self,
        output_dir: str = None,
        swagger_coverage_config: str = None,
        link_to_swagger_json: str = None,
        app_swagger_json_output: str = None,
        ignore_requests: List[str] = None,
    ):
        self.output_dir = output_dir
        self.swagger_coverage_config = swagger_coverage_config
        self.link_to_swagger_json = link_to_swagger_json
        self.app_swagger_json_output = app_swagger_json_output
        self.ignore_requests = ignore_requests if ignore_requests else []
