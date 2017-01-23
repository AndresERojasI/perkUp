from . import base
import tornado.web
from core import models
import core.SSH.ssh_maker as SSH
import os, sys
import tornado.escape
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
import pprint
import pickle

__SSH_PATH__ = "static/ssh_keys/"
__TABLES_PATH__ = "databases/"


class CreateDatasource(base.BaseHandler):
    """
    This class handles the creation of the Data Sources
    """

    @tornado.web.authenticated
    def get(self):
        return self.render("datasources/create.html", errors=False, user=self.get_current_user())

    def post(self):
        # Get all the required arguments from the POST parameters
        ds_name = self.get_argument('ds_custom_name', None)
        ds_type = self.get_argument('ds_type', None)
        ds_host = self.get_argument('ds_host', None)
        ds_port = self.get_argument('ds_port', None)
        ds_schema = self.get_argument('ds_schema', None)
        ds_user = self.get_argument('ds_user', None)
        ds_password = self.get_argument('ds_password', None)
        ssh_server = self.get_argument('ssh_server', None)
        ssh_port = self.get_argument('ssh_port', None)
        ssh_user = self.get_argument('ssh_user', None)
        ssh_pass = self.get_argument('ssh_pass', None)

        # Get the user information from the secure cookie
        user = self.get_current_user()

        # Validate the minimum required fields
        if ds_name is None or ds_type is None or ds_host is None or ds_port is None:
            return self.render("datasources/create.html",
                               errors="There are errors in this form please check them and try again", user=user)

        # Obtain the Organization data from the cookie and look it up in the database, just to confirm
        organization_data = user['organization']
        session = self.get_session()
        organization = session.query(models.Organization) \
            .filter(models.Organization.id == organization_data['id']) \
            .first()

        # Generate the unique passphrase and create the public/private key pair
        ssh_key_pass_phrase = os.urandom(64)
        ssh_builder = SSH.SSHCreator()
        ssh_key_pub = ssh_builder.createKey(organization_data['id'], ssh_key_pass_phrase, ds_name)

        # Create the datasource or redirect with error
        datasource = models.Datasource(
            host=ds_host,
            port=ds_port,
            user=ds_user,
            name=ds_name,
            schema=ds_schema,
            password=ds_password,
            type=ds_type,
            ssh_server=ssh_server,
            ssh_port=ssh_port,
            ssh_user=ssh_user,
            ssh_password=ssh_pass,
            ssh_key_pub=ssh_key_pub,
            ssh_key_pass_phrase=ssh_key_pass_phrase,
            organization_datasource=organization
        )

        try:
            session.add(datasource)
            session.commit()
            url = '/datasource/update?ds_id={}'.format(datasource.id)
            self.redirect(url)
        except ValueError:
            return self.render(
                "datasources/create.html",
                errors="There was an error when trying to create this Datasource, please try again in a moment",
                user=user
                )


class UpdateDatasource(base.BaseHandler):
    """
    This class handles the update of a datasource
    """
    @tornado.web.authenticated
    def get(self):
        # Get all the required arguments from the GET parameters
        ds_id = self.get_argument('ds_id', None)

        # Get the user information from the secure cookie
        user = self.get_current_user()
        organization_data = user['organization']
        if ds_id == None:
            return self.render(
                "datasources/update.html",
                errors="Please pass a Datasource ID",
                user=user,
                datasource=False
            )

        session = self.get_session()
        datasource = session.query(models.Datasource) \
            .filter(models.Datasource.id == ds_id and models.Datasource.organization_id == organization_data['id']) \
            .one_or_none()

        # Validate if a datasource id was passed
        if datasource is None:
            return self.render(
                "datasources/update.html",
                errors="No Datasource with that ID in this organization",
                user=user,
                datasource=False
            )

        return self.render(
            "datasources/update.html",
            errors=False,
            user=user,
            datasource=datasource
        )

    def post(self):
        # Get all the required arguments from the POST parameters
        ds_type = self.get_argument('ds_type', None)
        ds_host = self.get_argument('ds_host', None)
        ds_port = self.get_argument('ds_port', None)
        ds_schema = self.get_argument('ds_schema', None)
        ds_user = self.get_argument('ds_user', None)
        ds_password = self.get_argument('ds_password', None)
        ssh_server = self.get_argument('ssh_server', None)
        ssh_port = self.get_argument('ssh_port', None)
        ssh_user = self.get_argument('ssh_user', None)
        ssh_pass = self.get_argument('ssh_pass', None)
        ds_id = self.get_argument('ds_id', None)

        # Get the user information from the secure cookie
        user = self.get_current_user()
        if ds_id is None:
            return self.render(
                "datasources/update.html",
                errors="Please pass a Datasource ID",
                user=user,
                datasource=False
            )

        # Obtain the Organization data from the cookie and look it up in the database, just to confirm
        organization_data = user['organization']
        try:
            session = self.get_session()
            datasource = session.query(models.Datasource) \
                .filter(models.Datasource.id == ds_id, models.Datasource.organization_id == organization_data['id']) \
                .first()

            datasource.host = ds_host
            datasource.port = ds_port
            datasource.user = ds_user
            datasource.schema = ds_schema
            datasource.password = ds_password
            datasource.type = ds_type
            datasource.ssh_server = ssh_server
            datasource.ssh_port = ssh_port
            datasource.ssh_user = ssh_user
            datasource.ssh_password = ssh_pass

            session.add(datasource)
            session.commit()

        except ValueError:
            return self.render(
                "datasources/update.html",
                errors="Please pass a Datasource ID",
                user=user,
                datasource=False
            )

        url = '/datasource/update?ds_id={}'.format(organization_data['id'])
        self.redirect(url)

class TestDatasource(base.BaseHandler):
    def get(self):
        user = self.get_current_user()
        organization_data = user['organization']
        db_path = __TABLES_PATH__ + str(organization_data['id']) + '/tables/employees.table'
        table = pickle.load(open(db_path, "rb"))
        ds_id = self.get_argument('ds_id', None)
        session = self.get_session()
        datasource = session.query(models.Datasource) \
            .filter(models.Datasource.id == ds_id) \
            .one_or_none()
        file_path = "{}{}/{}/".format(__SSH_PATH__, organization_data['id'], datasource.name)
        server = SSHTunnelForwarder(
            (datasource.ssh_server, int(datasource.ssh_port)),
            ssh_username=datasource.ssh_user,
            ssh_pkey=file_path + 'private.key',
            ssh_private_key_password=datasource.ssh_key_pass_phrase,
            remote_bind_address=(datasource.host, int(datasource.port))
        )

        server.start()

        db_url = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(datasource.user, datasource.password, datasource.host,
                                                         server.local_bind_port, datasource.schema)
        engine = create_engine(db_url, pool_recycle=360)
        with engine.connect() as con:
            result = con.execute(table.count())
            for row in result:
                pprint.pprint(row)
