import base64
import json
from json import JSONDecodeError
from cryptography.fernet import Fernet
from data import Config

class FileOps(object):
    key = base64.urlsafe_b64encode(Config.JSON_SECRET_KEY.encode())
    fernet = Fernet(key)

    def file_operations_encrypted(operation, f, data=None):
        try:
            if operation == "read":
                data = f.read().decode()
                data = json.loads(data)["encrypted"]
                decrypted = FileOps.fernet.decrypt(data.encode()).decode()
                return json.loads(decrypted)
            else:
                f.seek(0)
                encrypted = json.dumps(data).encode()
                encrypted = FileOps.fernet.encrypt(encrypted).decode()
                write = {"encrypted": encrypted}
                f.write(json.dumps(write).encode())
                f.truncate()
                f.close()
                return True
        except JSONDecodeError:
            return False
        except KeyError:
            return False

    def file_operations_plain(operation, f, data=None):
        try:
            if operation == "read":
                return json.load(f)
            else:
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                f.close()
                # return True
        except JSONDecodeError:
            return False
        except KeyError:
            return False