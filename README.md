# swagger-coverage-py

### This project is the adapter which allows using [swagger-coverage](https://github.com/viclovsky/swagger-coverage) tool in Python projects (PyTest+Requests).

## Original description summary:

> Swagger-coverage gives a full picture about coverage of API tests (regression) based on OAS 2 (Swagger). By saying coverage we mean not a broad theme functionality, but presence (or absence) of calls defined by API methods, parameters, return codes or other conditions which corresponds specification of API.

Some more info about the project you can also
find [HERE](https://viclovsky.github.io/%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D0%B5%D1%81%D1%82%D1%8B%20%D0%BD%D0%B0%20api/2020/01/16/swagger-coverage)
<br>
<img src="https://raw.githubusercontent.com/JamalZeynalov/swagger-coverage-py/master/images/swagger-coverage-report.png" width=1100>

# How to use:

### 1. Create and place `swagger-coverage-config.json` file to your project:

Examples of configuration options you can find
in [Configuration options](https://github.com/viclovsky/swagger-coverage#configuration-options) section of the original
tool documentation.
> #### Note: This config is not required. You can skip this step and use the default behavior.
> #### Also, you can change the name and location of this file if you want.

### 2. Create `swagger-coverage-adapter-config.json` file in your project root:

```.json
{
  "output_dir": "swagger-coverage-output",
  "swagger_coverage_config": "swagger-coverage-config.json",
  "link_to_swagger_json": "https://petstore.swagger.io/v2/swagger.json",
  "ignore_requests": [
    "*any-part-of-request-name*",
  ]
}
```

* **output_dir** - Path from your project root to the output folder. The tool will automatically create this folder and save all recorded JSON files there.
* **swagger_coverage_config** - Path to your `swagger-coverage-config.json` file. Set the value `false` to use default config.
* **link_to_swagger_json** - HTTP(s) link to your OpenApi/Swagger documentation in JSON format. Adapted `swagger.json`
  file will be created in your project root.
* **ignore_requests** - all files matching any of listed masks will be removed before the report generation.

### 3. Add the session scoped fixture

```python
@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    runner = Runner()
    runner.cleanup_input_files()
    runner.setup()
    yield
    runner.generate_report()
```

> #### Note: If your API requires authentication then pass auth as an argument.
> #### Example:
> ```python 
> runner.setup(auth=HTTPBasicAuth("username", "password"))
> ```
> This is required to download swagger.json

### 3. Add the session scoped fixture

```python
from requests import Response
from requests.auth import HTTPBasicAuth
from swagger_coverage_py.listener import CoverageListener

response: Response = CoverageListener(
    method="get",
    base_url="https://petstore.swagger.io",
    raw_path="/v2/store/order/{orderId}",
    uri_params={"orderId": 1},
    auth=HTTPBasicAuth("username", "password"),
    params={"type": "active"},
).response
```
> #### Note: "auth" and "params" arguments are not required. <br>You can use any other **kwargs that are applicable for Requests library.

# How it works:
0. The fixture `setup_swagger_coverage` setups required artifacts
1. During test execution the CoverageListener saves all requests as JSON files in swagger format.
2. After the test execution the `Runner().generate_report()` creates a new report and saves it into your project root.

> #### Note: The `swagger-coverage-report.html` file depends on `swagger-coverage-results.json`.
> #### You should keep them together if you want to send this report via email.
