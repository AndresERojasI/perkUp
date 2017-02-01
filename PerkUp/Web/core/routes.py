from handlers import home, auth, datasources


def get_routes():

    app_routes = [
        # Format: (<path>, <handler>, [dict(<request handler kwargs>)])
        # e.g.: (r"^/hello/(\w+)$", handlers.GreetingHandler)
        (r"^/$", home.HomeHandler),
        (r"^/login$", auth.AuthHandler),
        (r"^/organization/create$", auth.OrganizationCreationHandler),
        (r"^/organization/createAdmin$", auth.CreateAdminHandler),
        (r"^/organization/validate_subdomain$", auth.ValidateSubdomain),
        (r"^/datasource/list$", datasources.ListDatasources),
        (r"^/datasource/create$", datasources.CreateDatasource),
        (r"^/datasource/update$", datasources.UpdateDatasource),
        (r"^/datasource/delete$", datasources.DeleteDatasource),
        (r"^/datasource/test$", datasources.TestDatasource),
        (r"^(.+)$", home.NotFoundHandler),
    ]

    return app_routes
