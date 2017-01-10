from . import base
import tornado.web
from web_core import models
import web_core.SSH.ssh_maker as SSH
import os
import tornado.escape
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine


__UPLOADS__ = "static/ssh_keys/"

class CreateDatasource(base.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.render("datasources/create.html", errors=False, user=self.get_current_user())

    def post(self):
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

        user = self.get_current_user()
        if ds_name == None or ds_type == None or ds_host == None or ds_port == None:
            return self.render("datasources/create.html",
                               errors="There are errors in this form please check them and try again", user=user)

        organization_data = user['organization']
        session = self.get_session()
        organization = session.query(models.Organization) \
            .filter(models.Organization.id == organization_data['id']) \
            .first()

        ssh_key_pass_phrase = os.urandom(64)

        sshBuilder = SSH.SSHCreator()
        ssh_key_pub = sshBuilder.createKey(organization_data['id'],ssh_key_pass_phrase, ds_name)

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
            return self.render("datasources/create.html",
                               errors="There was an error when trying to create this Datasource, please try again in a moment", user=user)


class UpdateDatasource(base.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        ds_id = self.get_argument('ds_id', None)
        user=self.get_current_user()
        organization_data = user['organization']
        if ds_id == None:
            return self.render(
                "datasources/update.html",
                errors="Please pass an Datasource ID",
                user=self.get_current_user(),
                datasource=False
            )

        session = self.get_session()
        datasource = session.query(models.Datasource) \
            .filter(models.Datasource.id == ds_id) \
            .one_or_none()

        connection_test = None
        try:
            file_path = "{}{}/{}/".format(__UPLOADS__, organization_data['id'], datasource.name)

            server = SSHTunnelForwarder(
                (datasource.ssh_server, int(datasource.ssh_port)),
                ssh_username=datasource.ssh_user,
                ssh_pkey=file_path+'private.key',
                ssh_private_key_password=datasource.ssh_key_pass_phrase,
                remote_bind_address=(datasource.host, int(datasource.port))
            )

            server.start()

            db_url = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(datasource.user, datasource.password, datasource.host, server.local_bind_port, datasource.schema)
            engine = create_engine(db_url, pool_recycle=360)
            with engine.connect() as con:

                rs = con.execute('SHOW TABLES')

                for row in rs:
                    print row

                con.close()
            server.stop()
        except Exception, e:
            print "Error: -------------"
            print str(e)
            print "-------------"
            connection_test = None


        if datasource == None:
            return self.render(
                "datasources/update.html",
                errors="There are no Datasources with that ID",
                user=self.get_current_user(),
                datasource=False
            )

        return self.render(
            "datasources/update.html",
            errors=False,
            user=user,
            datasource=datasource
        )