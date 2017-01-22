import os
import pickle
from sqlalchemy.ext.automap import automap_base
from core import models, SSH

__TABLES_PATH__ = "databases/"
class MapDatabase():
    def startMapping(self, organization_data):

        secureConnection = SSH.SSHConnection()

        with secureConnection.secureDBConnection() as conn:
            Base = automap_base()
            Base.prepare(conn, reflect=True)

            for table in Base.metadata.tables.items():
                db_path = __TABLES_PATH__ + str(organization_data['id']) + '/tables/'

                print "Path:", db_path
                if os.path.exists(db_path) != True:
                    os.makedirs(db_path, 0o777)

                with open(db_path + str(table[0]) + ".table", 'wb') as content_file:
                    content_file.write(pickle.dumps(table[1]))

            conn.close()

        secureConnection.closeConnection()