from . import base
import tornado
import simplejson as json

class HomeHandler(base.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = json.loads(self.get_secure_cookie('user'))

        return self.render("index.html", user = user)

class NotFoundHandler(base.BaseHandler):
    """
    Handler intended to catch all invalid paths. This way we raise a
    404 exception and show the appropriate not found error page.
    """

    def get(self, path):
        raise tornado.web.HTTPError(404)
