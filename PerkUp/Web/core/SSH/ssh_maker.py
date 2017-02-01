from Crypto.PublicKey import RSA
from os import chmod
import os

__UPLOADS__ = "static/ssh_keys/"


class SSHCreator:

    def __init__(self):
        pass

    def create_key(self, orgId, ds_name):

        file_path = "{}{}/{}/".format(__UPLOADS__, orgId, ds_name)
        if os.path.exists(file_path) != True:
            os.makedirs(file_path, 0o777)

        key = RSA.generate(2048)
        with open(file_path+"private.key", 'w') as content_file:
            chmod(file_path+"private.key", 0600)
            content_file.write(key.exportKey('PEM'))
        pubkey = key.publickey()
        with open(file_path+"public.key", 'w') as content_file:
            content_file.write(pubkey.exportKey('OpenSSH'))

        with open(file_path+"public.key", 'r') as content_file:
            content = content_file.read()

        return content
