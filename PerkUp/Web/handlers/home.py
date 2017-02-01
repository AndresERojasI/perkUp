from . import base
import tornado
from core import models

class HomeHandler(base.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        session = self.get_session()
        datasources = session.query(models.Datasource) \
            .all()
        return self.render("index.html", user=user, datasources=datasources)

class NotFoundHandler(base.BaseHandler):
    """
    Handler intended to catch all invalid paths. This way we raise a
    404 exception and show the appropriate not found error page.
    """

    def get(self, path):
        raise tornado.web.HTTPError(404)
