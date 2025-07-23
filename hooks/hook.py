import falcon

def auth_required(req, resp, resource, params):
    token = req.get_header('Authorization')
    if token != "TEST_TOKEN":
        raise falcon.HTTPUnauthorized(description="Invalid or missing token.")
