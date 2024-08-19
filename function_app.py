import json
import os

import azure.functions as func
from simian.entrypoint import entry_point_deploy

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

simian_app = {
    "route": "hello-world",
    "namespace": "apps.hello_world"
}

# route is the part after the prefix (default: api/)
@app.route(route=simian_app["route"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    request_data = req.get_json()
    response = entry_point_deploy(simian_app["namespace"], request_data)

    return func.HttpResponse(json.dumps(response), status_code=200)
