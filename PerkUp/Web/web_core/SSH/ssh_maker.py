from Crypto.PublicKey import RSA
import os

__UPLOADS__ = "static/ssh_keys/"

class SSHCreator():
    def createKey(self, orgId, passPhrase, ds_name ):
        key = RSA.generate(2048)
        encrypted_key = key.exportKey(passphrase=passPhrase, pkcs=8,
                                      protection="scryptAndAES128-CBC")
        file_path =  "{}{}/{}/".format(__UPLOADS__, orgId, ds_name)

        if os.path.exists(file_path) != True:
            os.makedirs(file_path, 0o777)

        file_out = open(file_path + "rsa_key.bin", "wb")
        file_out.write(encrypted_key)

        return key.publickey().exportKey()