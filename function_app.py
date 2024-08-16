import azure.functions as func
import json
import logging
import traceback
import os

from simian.entrypoint import entry_point
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# simian.json contains simian specific app info
# for example a route to namespace mapping
simian_json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'simian.json')
f = open(simian_json_file) 
simian_info = json.load(f) 

namespaces = {}
for ns in simian_info["route-namespace-map"]:
    namespaces[ns["route"]] = ns

# route is the part after api/ and we call it api_slug
@app.route(route="{api_slug}")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

   
    try:
        request_data = req.get_json()
    except ValueError as exc:
        return func.HttpResponse(
            _create_error_response(
                "An error occurred when processing the request data: " + str(exc), exc
            ),
            status_code=200,
        )

    # Route the post to the entrypoint method.
    api_slug = req.route_params.get("api_slug")
    namespace = namespaces[api_slug]["namespace"]
    request_data[1].update({"namespace": namespace})

    try:
        # Call the entry_point to access the application with the request data.
        payload_out = entry_point(
            request_data[0], # operation
            request_data[1], # metadata
            request_data[2], # payload
        )

        # Defer loading the utils until the entry_point has checked that Simian GUI
        # can be used.
        from simian.gui import utils

        # Return the payload as a JSON string to Azure.
        response = f'{{"returnValue": {utils.payloadToString(payload_out)}}}'

    except Exception as exc:
        # Put the error message in the response.
        logging.error("Error caught by entrypoint wrapper: %r", exc)
        response = _create_error_response(str(exc), exc)

    return func.HttpResponse(response, status_code=200)


def _create_error_response(msg: str, exc: Exception) -> dict:
    """Create an error response dictionary from a caught exception."""
    return json.dumps(
        {
            "error": {
                "message": msg,
                "stacktrace": traceback.format_tb(exc.__traceback__),  # Optional
            }
        }
    )
