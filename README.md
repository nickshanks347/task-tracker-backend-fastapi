# task-tracker-backend-fastapi

[![Build & Push](https://github.com/nickshanks347/task-tracker-backend-fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/nickshanks347/task-tracker-backend-fastapi/actions/workflows/ci.yml)

This is a simple task tracker backend using FastAPI. It uses a simple bearer token authentication scheme but stores users/user files in JSON (with optional encryption).

## Installation

First, clone the repository:

```bash
git clone https://github.com/nickshanks347/task-tracker-backend-fastapi
```

`cd` into `task-tracker-backend-fastapi`:

```bash
cd task-tracker-backend-fastapi
```

*Optionally, create and enter a virtual environment:*

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

Copy the config file:

```bash
cd data
cp config_example.env config.env
```

---

## Configuration

The application needs `config.env` in order to start correctly.

Included in the repository is a `config_example.env`, stored in the data directory. It has this format:

```env
JWT_SECRET_KEY=secret
JSON_SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENABLE_REGISTRATIONS=1
ENCRYPT_JSON=1
RELOAD=1
HOST=0.0.0.0
PORT=8000
```

1. `JWT_SECRET_KEY` contains the secret key for the JWT authentication scheme.
2. `JSON_SECRET_KEY` contains the secret key for the JSON encryption scheme.
3. `ALGORITHM` contains the algorithm for the JWT authentication scheme.
4. `ACCESS_TOKEN_EXPIRE_MINUTES` contains the number of minutes the access token is valid for.
5. `ENABLE_REGISTRATIONS` contains whether or not registrations are enabled.
6. `ENCRYPT_JSON` contains whether or not JSON files are encrypted.
7. `RELOAD` contains whether or not the application should reload the Python files on-save (usually only enabled for debugging/development)
8. `HOST` contains the hostname to bind the application to.
9. `PORT` contains the port to bind the application to.

When the application starts, it will use `python-dotenv` to set the environment variables listed above. The application then reads the required environment variables and loads them into the application.

---

### Encryption/Decryption

**You should not use an insecure value for `JWT_SECRET_KEY` or `JSON_SECRET_KEY`, nor should you use the default value "`secret`"**.

To generate a secure value for `JWT_SECRET_KEY`, use the following command:

```bash
openssl rand -hex 32
```

To generate a secure value for `JSON_SECRET_KEY`, use the following command:

```bash
openssl rand -hex 16
```

Note: **`JSON_SECRET_KEY` needs a 32-bit key.**

A file to encrypt/decrypt JSON files is stored in the `data` directory. It is called `decrypt_encrypt.py`.

The file will read the `JSON_SECRET_KEY` from the `config.env` file and use it to encrypt/decrypt all JSON files in the `data` directory.

To encrypt all JSON files, use the following command:

```bash
python3 decrypt_encrypt.py --encrypt
```

To decrypt all JSON files, use the following command:

```bash
python3 decrypt_encrypt.py --decrypt
```

---

## Running the application

To run the application, simply enter `task-tracker-backend-fastapi` and run the following command:

```bash
python3 main.py
```

---

## Docker

The application is available on DockerHub at <https://hub.docker.com/r/nickshanks347/todo-fastapi>. You can pull the latest application with `docker pull nickshanks347/todo-fastapi:latest`. Each tag corresponds to a short Git commit hash.

Using the environment variables above, you can run the Docker image with the following command:

```bash
docker run -p 8000:8000 --name todo-fastapi -e JWT_SECRET_KEY=secret -e JSON_SECRET_KEY=secret -e ALGORITHM=HS256 -e ACCESS_TOKEN_EXPIRE_MINUTES=30 -e ENABLE_REGISTRATIONS=true -e ENCRYPT_JSON=true -v ./data:/code/data nickshanks347/todo-fastapi:latest
```

**Again, be sure to use a secure value for `JWT_SECRET_KEY` and `JSON_SECRET_KEY`.**

### Building Docker image

If you want to build the image locally, use the included Dockerfile:

```bash
docker build -t todo-fastapi .
```
