import base64
import os
from core.config import Config
import json
from cryptography.fernet import Fernet
import codecs


class StartupChecks(object):

    key = base64.urlsafe_b64encode(Config.JSON_SECRET_KEY.encode())
    fernet = Fernet(key)
    reader = codecs.getreader("utf-8")

    def startup_checks():
        print("Performing startup checks...")
        files = []
        for filename in os.listdir("./data/"):
            if filename.endswith(".json"):
                files.append(filename)
        print("Encryption enabled...") if Config.ENCRYPT_JSON else print(
            "Encryption disabled."
        )
        if "users.json" in files:
            print("users.json exists...")
            with open("./data/users.json", "rb") as f:
                try:
                    if Config.ENCRYPT_JSON:
                        data = f.read().decode()
                        data = json.loads(data)["encrypted"]
                        StartupChecks.fernet.decrypt(data.encode()).decode()
                    if not Config.ENCRYPT_JSON:
                        json.load(f)
                    print("users.json loaded successfully...")
                except (json.decoder.JSONDecodeError, KeyError):
                    f.close()
                    print("users.json is not valid JSON...")
                    print("Moving users.json to users.json.bak...")
                    os.rename("./data/users.json", "./data/users.json.bak")
                    print("Creating new users.json...")
                    with open("./data/users.json", "wb") as f:
                        f.write("{}".encode())
                    if Config.ENCRYPT_JSON:
                        print("Encrypting new users.json...")
                        json_file = json.load(f)
                        encrypted = json.dumps(json_file).encode()
                        encrypted = StartupChecks.fernet.encrypt(encrypted).decode()
                        write = {"encrypted": encrypted}
                        f.seek(0)
                        f.write(json.dumps(write, indent=4).encode())
                        f.truncate()
                        f.close()

        elif "users.json" not in files:
            print("users.json does not exist, creating new one...")
            with open("./data/users.json", "w") as f:
                json.dump({}, f)
            if Config.ENCRYPT_JSON:
                print("Encrypting new users.json...")
                with open("./data/users.json", "rb+") as f:
                    data = json.load(f)
                    encrypted = json.dumps(data).encode()
                    encrypted = StartupChecks.fernet.encrypt(encrypted).decode()
                    write = {"encrypted": encrypted}
                    f.seek(0)
                    f.write(json.dumps(write, indent=4).encode())
                    f.truncate()
                    f.close()
        with open("./data/users.json", "rb") as f:
            if Config.ENCRYPT_JSON:
                data = json.load(f)
                encrypted = data["encrypted"]
                encrypted = StartupChecks.fernet.decrypt(encrypted.encode()).decode()
                data = json.loads(encrypted)
            else:
                data = json.load(f)
        if data:
            print("Looping through user IDs...")
        else:
            print("No users found...")
        for user in data:
            id = data[user]["id"]
            if f"{id}.json" not in files:
                print(f"JSON file for user ID {id} does not exist, creating new one...")
                with open(f"./data/{id}.json", "w") as f:
                    json.dump({}, f)
                if Config.ENCRYPT_JSON:
                    print("Encrypting JSON file...")
                    with open(f"./data/{id}.json", "rb+") as f:
                        json_file = json.load(f)
                        encrypted = json.dumps(json_file).encode()
                        encrypted = StartupChecks.fernet.encrypt(encrypted).decode()
                        write = {"encrypted": encrypted}
                        f.seek(0)
                        f.write(json.dumps(write, indent=4).encode())
                        f.truncate()
                        f.close()
            else:
                print("JSON file for user ID {} exists...".format(id))
