import os
import pickle
from sqlalchemy.ext.automap import automap_base
from core import models, SSH

__TABLES_PATH__ = "databases/"


class MapDatabase:

    def start_mapping(self, datasource, org_id):

        secure_connection = SSH.SSHConnection()
        tables = []

        with secure_connection.secureDBConnection(datasource, org_id) as conn:
            Base = automap_base()
            Base.prepare(conn, reflect=True)

            for table in Base.metadata.tables.items():
                tables.append({
                    'table_name': table[0],
                    'serialized_table': pickle.dumps(table[1])
                })

            conn.close()

        secure_connection.closeConnection()

        return tables