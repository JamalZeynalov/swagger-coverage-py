class URI:
    def __init__(self, host: str, unformatted_path: str, **uri_params):
        self.host = host
        self.formatted = unformatted_path.format(**uri_params)
        self.full = f"{self.host}{self.formatted}"
        self.raw = unformatted_path
        self.uri_params: dict = uri_params
