import json
from http import HTTPStatus

import azure.functions as func
from simian.entrypoint import entry_point_deploy

# Define simian app:
# - route without azure function prefix (default: api/),
# - namespace of its module
simian_app_base_data = {"route": "hello-world-step-", "namespace": "apps.hello_world_step_"}

# Anonymous access for symplicity
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Route is the part after the prefix (default: api/)
@app.route(route=simian_app["route"] + "{step:int}")
def main(req: func.HttpRequest) -> func.HttpResponse:
    request_data = req.get_json()
    response = entry_point_deploy(
        simian_app["namespace"] + req.route_params.get("step"), request_data
    )

    return func.HttpResponse(json.dumps(response), status_code=HTTPStatus.OK)
