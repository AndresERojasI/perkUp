from handlers import home, auth

def getRoutes():

    app_routes = [
        # Format: (<path>, <handler>, [dict(<request handler kwargs>)])
        # e.g.: (r"^/hello/(\w+)$", handlers.GreetingHandler)
        (r"^/$", home.HomeHandler),
        (r"^/login$", auth.AuthHandler),
        (r"^/organization/create$", auth.OrganizationCreationHandler),
        (r"^/organization/createAdmin$", auth.CreateAdminHandler),
        (r"^/organization/validate_subdomain$", auth.ValidateSubdomain),
        (r"^(.+)$", home.NotFoundHandler),
    ]

    return app_routes