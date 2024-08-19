import json

import azure.functions as func
from simian.entrypoint import entry_point_deploy

# Define simian app:
# - route without azure function prefix (default: api/), 
# - namespace of its module
simian_app = {
    "route": "hello-world",
    "namespace": "app.hello_world"
}

# Anonymous access for symplicity
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Route is the part after the prefix (default: api/)
@app.route(route=simian_app["route"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    request_data = req.get_json()
    response = entry_point_deploy(simian_app["namespace"], request_data)

    return func.HttpResponse(json.dumps(response), status_code=200)
