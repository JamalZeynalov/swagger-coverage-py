import json
from typing import List

from singleton_decorator import singleton


@singleton
class AdapterConfig:
    def __init__(self, api_name: str = None):
        self.api_name = api_name

        with open(self.swagger_coverage_config, "r") as f:
            self.json_config: dict = json.loads(f.read())

        self.output_dir = f"swagger-coverage-output-{self.name}"

    @property
    def ignore_requests(self) -> List[str]:
        ignore_list = self.json_config.get("ignore_requests")
        return ignore_list if ignore_list else []

    @property
    def swagger_coverage_config(self):
        return f"{self.json_config.get('swagger_coverage_config')}-{self.api_name}.json"
