import json
import os
import logging

import azure.functions as func

from simian.entrypoint import entry_point_deploy

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# route is the part after the prefix (default: api/)
@app.route(route="{api_slug}")
def main(req: func.HttpRequest) -> func.HttpResponse:
    request_route = req.route_params.get("api_slug")
    logging.info(f'Request route: {request_route}')
    # Route the post to the entrypoint method.
    namespace = get_namespace_by_slug(request_route)
    request_data = req.get_json()
    response = entry_point_deploy(namespace, request_data)

    return func.HttpResponse(json.dumps(response), status_code=200)


def get_namespace_by_slug(api_slug: str) -> str:
    # simian.json contains simian specific app info
    # a.o. the route to module namespace mapping
    simian_json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'simian.json')
    f = open(simian_json_file) 
    simian_info = json.load(f) 
     
    for route2ns in simian_info["route-namespace-map"]:
        if (route2ns['route'] == api_slug):
            namespace = route2ns['namespace']
            break
    
    return namespace
