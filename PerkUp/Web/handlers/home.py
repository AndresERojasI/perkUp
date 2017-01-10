from . import base
import tornado
import simplejson as json

class HomeHandler(base.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.render("index.html", user = self.get_current_user())

class NotFoundHandler(base.BaseHandler):
    """
    Handler intended to catch all invalid paths. This way we raise a
    404 exception and show the appropriate not found error page.
    """

    def get(self, path):
        raise tornado.web.HTTPError(404)
