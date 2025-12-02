from flask import request, redirect

def register_middlewear(app):

    @app.before_request
    def check_authentication():

        public_routes = ["login", "register", "index", "static","show_map"]

        if request.endpoint and request.endpoint.split(".")[-1] in public_routes:
            return None

        token = request.cookies.get("auth")
        if token is None:
            return redirect("/login")
