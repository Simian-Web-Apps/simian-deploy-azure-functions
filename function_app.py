import json
import azure.functions as func
import os

from simian.entrypoint import entry_point_deploy

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# simian.json contains simian specific app info
# a.o. the route to module namespace mapping
simian_json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'simian.json')
f = open(simian_json_file) 
simian_info = json.load(f) 

namespaces = {}
for ns in simian_info["route-namespace-map"]:
    namespaces[ns["route"]] = ns
    
# route is the part after the prefix (default: api/)
@app.route(route="{api_slug}")
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Route the post to the entrypoint method.
    api_slug = req.route_params.get("api_slug")
    namespace = namespaces[api_slug]["namespace"]
    
    request_data = req.get_json()
    response = entry_point_deploy(namespace, request_data)

    return func.HttpResponse(json.dumps(response), status_code=200)
