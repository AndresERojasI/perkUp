"""
Defines the base controller that all of the bootstrap controllers inherit from
"""

from sqlalchemy.orm import sessionmaker
import tornado.web
from web_core import models
import simplejson as json


class BaseHandler(tornado.web.RequestHandler):
    db_session = None

    def get_current_user(self):
        user = self.get_secure_cookie('user')

        return json.loads(user) if user != None else None

    def get_session(self):
        if self.db_session is None:
            DBSession = sessionmaker(bind=models.engine)
            self.db_session = DBSession()

        return self.db_session
