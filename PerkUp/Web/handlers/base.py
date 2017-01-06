"""
Defines the base controller that all of the bootstrap controllers inherit from
"""

import os, uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import tornado.web
from web_core import models


class BaseHandler(tornado.web.RequestHandler):
    db_session = None

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_session(self):
        if self.db_session is None:
            DBSession = sessionmaker(bind=models.engine)
            self.db_session = DBSession()

        return self.db_session
