# swagger-coverage-py

### This project is the adapter that allows using [swagger-coverage](https://github.com/viclovsky/swagger-coverage) tool in Python projects (PyTest+Requests).

## Original description summary:

> Swagger-coverage gives a full picture about coverage of API tests (regression) based on OAS 2 (Swagger). By saying coverage we mean not a broad theme functionality, but presence (or absence) of calls defined by API methods, parameters, return codes or other conditions which corresponds specification of API.

Some more info about the project you can also
find [HERE](https://viclovsky.github.io/%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D0%B5%D1%81%D1%82%D1%8B%20%D0%BD%D0%B0%20api/2020/01/16/swagger-coverage)
<br>
<img src="https://raw.githubusercontent.com/JamalZeynalov/swagger-coverage-py/master/images/swagger-coverage-report.png" width=1100>

# How to use:

### 1. Install `swagger-coverage-py` as a project requirement.

```shell
pip install -e git+ssh://git@github.com/JamalZeynalov/swagger-coverage-py.git#egg=swagger_coverage
```

or just add the dependency to requirements.txt

```text
-e git+ssh://git@github.com/JamalZeynalov/swagger-coverage-py.git#egg=swagger_coverage
```

### 2. Add the session-scoped fixture

```python
import pytest
from swagger_coverage_py.runner import Runner
from requests.auth import HTTPBasicAuth


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    runner = Runner(api_name="my-project", host="http://my-project.com")
    runner.cleanup_input_files()
    runner.setup("/api/v1/resources/my_project/doc/swagger.json", auth=HTTPBasicAuth("username", "password"))

    yield
    runner.generate_report()
```

#### If you have 2 and more projects, then just add more runners:

```python
import pytest
from swagger_coverage_py.runner import Runner
from requests.auth import HTTPBasicAuth


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    runner = Runner(api_name="petstore", host="https://petstore.swagger.io")
    runner.cleanup_input_files()
    runner.setup(path_to_swagger_json="/v2/swagger.json")

    runner2 = Runner(api_name="my-project", host="http://my-project.com")
    runner2.cleanup_input_files()
    runner2.setup(path_to_swagger_json="/api/v1/swagger.json", auth=HTTPBasicAuth("username", "password"))

    yield
    runner.generate_report()
    runner2.generate_report()
```

> #### Steps and Parameters:
> `api_name` - Define the name of the API. This name will be used to define a configuration file (see below).<br>
> &nbsp;&nbsp;&nbsp;&nbsp; Here they are `swagger-coverage-config-petstore.json` and `swagger-coverage-config-my-project.json`.<br>
>
> `host` - The host of the API.
> It will be used to download a swagger.json file and to identify the CoverageListener output directory for each API.
>
> `cleanup_input_files()` - Deletes all files in the CoverageListener output directory (according to the called API host)
>
> `path_to_swagger_json` - A second part of the HTTP link to your OpenApi/Swagger documentation in JSON format
> &nbsp;&nbsp;&nbsp;&nbsp; Adapted `swagger-<api_name>.json` file will be created in your project root.
> `auth` - An authentication parameter for "requests" lib. Skip it if your API doesn't require authentication.

### 3. Create and place `swagger-coverage-config-<api_name>.json` file(s) to your project:

```json
{
  "rules": {
    "status": {
      "enable": true,
      "ignore": [
        "500"
      ],
      "filter": []
    },
    "only-declared-status": {
      "enable": false
    },
    "exclude-deprecated": {
      "enable": true
    }
  },
  "writers": {
    "html": {
      "locale": "en",
      "filename": "swagger-coverage-report-petstore.html"
    }
  }
}
```

> ### If you have more than 1 API then this config MUST:
> #### 1. Be created for each microservice which you track using `CoverageListener`.
> Otherwise, the default behavior will be applied, and your report will be saved as `swagger-coverage-report.html` which may cause override in case you have multiple APIs
> #### 2. Contain `writers` section with filename in the format: `swagger-coverage-report-<api_name>.html`
> #### 3. Be placed in the root of your project

More examples of configuration options you can find in
the [Configuration options](https://github.com/JamalZeynalov/swagger-coverage#configuration-options) section of the
documentation.

### 4. Trace all your API calls with CoverageListener:

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

### 5. Run your tests and open created `swagger-coverage-report.html` in your browser.

# How it works:

1. The fixture `setup_swagger_coverage` setups required artifacts
2. During test execution the CoverageListener saves all requests as JSON files in swagger format to a subdirectory named
   as a called host. (e.g. `swagger-coverage-output/petstore.swagger.io/`). 
3. After all tests execution a `Runner().generate_report()` creates and saves new report(s) into your project root.

## Created & Maintained By

[Jamal Zeinalov](https://github.com/JamalZeynalov)

## License

Swagger coverage is released under version 2.0 of the [Apache License](http://www.apache.org/licenses/LICENSE-2.0)