import argparse
import base64
from cryptography.fernet import Fernet
import os
from __init__ import Config
import json

parser = argparse.ArgumentParser(description='Decrypt and encrypt data files for backend')
parser.add_argument('-d', '--decrypt', help='Decrypt data files', action='store_true')
parser.add_argument('-e', '--encrypt', help='Encrypt data files', action='store_true')
args = parser.parse_args()

key = base64.urlsafe_b64encode(Config.JSON_SECRET_KEY.encode())
fernet = Fernet(key)

if args.decrypt and args.encrypt:
    print("You can only decrypt or encrypt, not both")
    exit(1)
elif args.decrypt:
    print("Decrypting data files")
    for filename in os.listdir():
        if filename.endswith(".json"):
            with open(filename, "rb+") as f:
                data = f.read().decode()
                data = json.loads(data)["encrypted"]
                decrypted = fernet.decrypt(data.encode()).decode()
                f.seek(0)
                f.write(json.dumps(json.loads(decrypted), indent=4).encode())
                f.truncate()
                f.close()
    exit(0)
elif args.encrypt:
    print("Encrypting data files")
    for filename in os.listdir():
        if filename.endswith(".json"):
            with open(filename, "rb+") as f:
                data = json.load(f)
                encrypted = json.dumps(data).encode()
                encrypted = fernet.encrypt(encrypted).decode()
                write = {"encrypted": encrypted}
                f.seek(0)
                f.write(json.dumps(write, indent=4).encode())
                f.truncate()
                f.close()
    exit(0)