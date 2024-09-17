# see: https://doc.simiansuite.com/simian-gui/deployment/python.html#azure-functions
import json
from http import HTTPStatus

import azure.functions as func
from simian.entrypoint import entry_point_deploy

# Anonymous access for symplicity
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Route is the part after the prefix (default: api/)
# Define the route with a numeric parameter "step" to facilitate multiple hello-world steps
@app.route(route="{app}")
def main(req: func.HttpRequest) -> func.HttpResponse:
    request_data = req.get_json()
    # Compose the simian app module namespace from base namespace and route parameter "step".
    app_module_namespace = "apps." + req.route_params.get("app")
    response = entry_point_deploy(app_module_namespace, request_data)

    return func.HttpResponse(json.dumps(response), status_code=HTTPStatus.OK)
