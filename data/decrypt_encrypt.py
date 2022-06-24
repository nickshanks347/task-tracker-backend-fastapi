import argparse
import base64
from cryptography.fernet import Fernet
import os
from core.config import Config
import json
import colorama

parser = argparse.ArgumentParser(
    description="Decrypt and encrypt data files for backend"
)
parser.add_argument("-d", "--decrypt", help="Decrypt data files", action="store_true")
parser.add_argument("-e", "--encrypt", help="Encrypt data files", action="store_true")
args = parser.parse_args()

key = base64.urlsafe_b64encode(Config.JSON_SECRET_KEY.encode())
fernet = Fernet(key)
colorama.init()
try:
    if not args.decrypt and not args.encrypt:
        print(colorama.Fore.RED + " :: Please specify either --decrypt or --encrypt")
        exit(1)
    if args.decrypt and args.encrypt:
        print(colorama.Fore.RED + " :: You can only decrypt or encrypt, not both")
        exit(1)
    elif args.decrypt:
        try:
            for filename in os.listdir():
                if filename.endswith(".json"):
                    print(colorama.Fore.GREEN + f" :: Decrypting {filename}")
                    with open(filename, "rb+") as f:
                        data = f.read().decode()
                        data = json.loads(data)["encrypted"]
                        decrypted = fernet.decrypt(data.encode()).decode()
                        f.seek(0)
                        f.write(json.dumps(json.loads(decrypted), indent=4).encode())
                        f.truncate()
                        f.close()
            exit(0)
        except KeyError:
            print(colorama.Fore.RED + " :: Data is already decrypted")
    elif args.encrypt:
        for filename in os.listdir():
            if filename.endswith(".json"):
                print(colorama.Fore.GREEN + f" :: Encrypting {filename}")
                with open(filename, "rb+") as f:
                    data = json.load(f)
                    if data.get("encrypted"):
                        print(colorama.Fore.RED + " :: Data is already encrypted")
                        exit(0)
                    encrypted = json.dumps(data).encode()
                    encrypted = fernet.encrypt(encrypted).decode()
                    write = {"encrypted": encrypted}
                    f.seek(0)
                    f.write(json.dumps(write, indent=4).encode())
                    f.truncate()
                    f.close()
        exit(0)
finally:
    colorama.Style.RESET_ALL
