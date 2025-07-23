import falcon

class AuthMiddleware:
    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        if token != "TEST_TOKEN":
            raise falcon.HTTPUnauthorized(
                title="Unauthorized",
                description="Invalid or missing token."
            )

app = falcon.App(middleware=[AuthMiddleware()])
