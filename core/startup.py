import base64
import codecs
import json
import os
from pathlib import Path

from cryptography.fernet import Fernet

from core.config import Config


class StartupChecks(object):

    key = base64.urlsafe_b64encode(Config.JSON_SECRET_KEY.encode("utf-8"))
    fernet = Fernet(key)
    reader = codecs.getreader("utf-8")

    def startup_checks():
        DATA_DIR = Config.DATA_DIR
        print("Performing startup checks...")
        files = []
        for filename in os.listdir(Path(__file__).parent.parent / DATA_DIR):
            if filename.endswith(".json"):
                files.append(filename)
        print("Encryption enabled...") if Config.ENCRYPT_JSON else print(
            "Encryption disabled."
        )
        if "users.json" in files:
            print("users.json exists...")
            with open(f"{DATA_DIR}/users.json", "rb") as f:
                try:
                    if Config.ENCRYPT_JSON:
                        data = f.read().decode("utf-8")
                        data = json.loads(data)["encrypted"]
                        StartupChecks.fernet.decrypt(data.encode("utf-8")).decode(
                            "utf-8"
                        )
                    if not Config.ENCRYPT_JSON:
                        json.load(f)
                    print("users.json loaded successfully...")
                except (json.decoder.JSONDecodeError):
                    f.close()
                    print("users.json is not valid JSON...")
                    print("Moving users.json to users.json.bak...")
                    os.rename(f"{DATA_DIR}/users.json", f"{DATA_DIR}/users.json.bak")
                    print("Creating new users.json...")
                    with open(f"{DATA_DIR}/users.json", "wb") as f:
                        f.write("{}".encode("utf-8"))
                    if Config.ENCRYPT_JSON:
                        print("Encrypting new users.json...")
                        json_file = json.load(f)
                        encrypted = json.dumps(json_file).encode("utf-8")
                        encrypted = StartupChecks.fernet.encrypt(encrypted).decode(
                            "utf-8"
                        )
                        write = {"encrypted": encrypted}
                        f.seek(0)
                        f.write(json.dumps(write, indent=4).encode("utf-8"))
                        f.truncate()
                        f.close()

        elif "users.json" not in files:
            print("users.json does not exist, creating new one...")
            with open(f"{Path(__file__).parent.parent / DATA_DIR}/users.json", "w") as f:
                json.dump({}, f)
            if Config.ENCRYPT_JSON:
                print("Encrypting new users.json...")
                with open(
                    f"{Path(__file__).parent.parent / DATA_DIR}/users.json", "rb+"
                ) as f:
                    data = json.load(f)
                    encrypted = json.dumps(data).encode("utf-8")
                    encrypted = StartupChecks.fernet.encrypt(encrypted).decode("utf-8")
                    write = {"encrypted": encrypted}
                    f.seek(0)
                    f.write(json.dumps(write, indent=4).encode("utf-8"))
                    f.truncate()
                    f.close()
        with open(f"{Path(__file__).parent.parent / DATA_DIR}/users.json", "rb") as f:
            if Config.ENCRYPT_JSON:
                data = json.load(f)
                encrypted = data["encrypted"]
                encrypted = StartupChecks.fernet.decrypt(
                    encrypted.encode("utf-8")
                ).decode("utf-8")
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
                with open(
                    f"{Path(__file__).parent.parent / DATA_DIR}/{id}.json", "w"
                ) as f:
                    json.dump({}, f)
                if Config.ENCRYPT_JSON:
                    print("Encrypting JSON file...")
                    with open(
                        f"{Path(__file__).parent.parent / DATA_DIR}/{id}.json", "rb+"
                    ) as f:
                        json_file = json.load(f)
                        encrypted = json.dumps(json_file).encode("utf-8")
                        encrypted = StartupChecks.fernet.encrypt(encrypted).decode(
                            "utf-8"
                        )
                        write = {"encrypted": encrypted}
                        f.seek(0)
                        f.write(json.dumps(write, indent=4).encode("utf-8"))
                        f.truncate()
                        f.close()
            else:
                print("JSON file for user ID {} exists...".format(id))
