from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine

__SSH_PATH__ = "static/ssh_keys/"

class SSHConnection():
    server = None
    def secureDBConnection(self, datasource, org_id):

        file_path = "{}{}/{}/".format(__SSH_PATH__, org_id, datasource.name)
        self.server = SSHTunnelForwarder(
            (datasource.ssh_server, int(datasource.ssh_port)),
            ssh_username=datasource.ssh_user,
            ssh_pkey=file_path + 'private.key',
            ssh_private_key_password=datasource.ssh_key_pass_phrase,
            remote_bind_address=(datasource.host, int(datasource.port))
        )

        self.server.start()

        engine = create_engine(self.getConnectionString(datasource), pool_recycle=360)

        return engine.connect()

    def closeConnection(self):
        self.server.stop()

    def getConnectionString(self, datasource):
        conn_strings = {
            'PostgreSQL': 'postgresql://{}:{}@{}:{}/{}'.format(
                datasource.user,
                datasource.password,
                datasource.host,
                self.server.local_bind_port,
                datasource.schema
            ),
            'Firebird': 'firebird+fdb://{}:{}@{}:{}/{}'.format(
                datasource.user,
                datasource.password,
                datasource.host,
                self.server.local_bind_port,
                datasource.schema
            ),
            'Microsoft SQL Server': 'mssql+pyodbc://{}:{}@{}:{}'.format(
                datasource.user,
                datasource.password,
                datasource.host,
                self.server.local_bind_port
            ),
            'MySQL': 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(
                datasource.user,
                datasource.password,
                datasource.host,
                self.server.local_bind_port,
                datasource.schema
            ),
            'Oracle': 'oracle://{}:{}@{}:{}/{}'.format(
                datasource.user,
                datasource.password,
                datasource.host,
                self.server.local_bind_port,
                datasource.schema
            ),
            'Sybase': 'sybase+pysybase://{}:{}@{}:{}/{}'.format(
                datasource.user,
                datasource.password,
                datasource.host,
                self.server.local_bind_port,
                datasource.schema
            )
        }

        return conn_strings[datasource.type]
