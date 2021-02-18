import json
from typing import List


class AdapterConfig:
    def __init__(self, api_name: str = None):
        self.api_name = api_name
        self.output_dir = f"swagger-coverage-output-{self.api_name}"
        self.swagger_coverage_config = f"swagger-coverage-config-{self.api_name}.json"

    @property
    def ignore_requests(self) -> List[str]:
        if not getattr(self, "ignore_requests", None):
            with open(self.swagger_coverage_config, "r") as f:
                json_config: dict = json.loads(f.read())

            ignore_list = json_config.get("ignore_requests")
            return ignore_list if ignore_list else []
