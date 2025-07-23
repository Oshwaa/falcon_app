import falcon

def handle_value_error(req, resp, exc, params):
    resp.status = falcon.HTTP_400
    resp.media = {"error": exc.errors()}  


def handle_unauthorized_error(req, resp, exc, params):
    resp.status = falcon.HTTP_401
    resp.media = {"description": "Invalid or missing auth token"}

def handle_generic_exception(req, resp, exc, params):
    resp.status = falcon.HTTP_500
    resp.media = {"error": "Something went wrong"}