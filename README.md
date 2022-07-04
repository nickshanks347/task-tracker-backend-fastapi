# task-tracker-backend-fastapi

[![Build & Push](https://github.com/nickshanks347/task-tracker-backend-fastapi/actions/workflows/main.yml/badge.svg)](https://github.com/nickshanks347/task-tracker-backend-fastapi/actions/workflows/main.yml) [![CodeQL](https://github.com/nickshanks347/task-tracker-backend-fastapi/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/nickshanks347/task-tracker-backend-fastapi/actions/workflows/codeql-analysis.yml) [![codecov](https://codecov.io/gh/nickshanks347/task-tracker-backend-fastapi/branch/main/graph/badge.svg?token=toWh5loMI9)](https://codecov.io/gh/nickshanks347/task-tracker-backend-fastapi)

This is a simple task tracker backend using FastAPI. It uses a simple bearer token authentication scheme with SQLite as the database.

## Installation

First, clone the repository:

```bash
git clone https://github.com/nickshanks347/task-tracker-backend-fastapi
```

`cd` into `task-tracker-backend-fastapi`:

```bash
cd task-tracker-backend-fastapi
```

Install dependencies:

```bash
poetry install --no-dev
```

*Optionally install development dependencies too:*

```bash
poetry install
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
DATA_DIR=data
```

1. `JWT_SECRET_KEY` contains the secret key for the JWT authentication scheme.
2. `ALGORITHM` contains the algorithm for the JWT encryption scheme.
3. `ACCESS_TOKEN_EXPIRE_MINUTES` contains the number of minutes the access token is valid for.
4. `ENABLE_REGISTRATIONS` contains whether or not registrations are enabled.
5. `RELOAD` contains whether or not the application should reload the Python files on saving (usually only enabled for debugging/development).
6. `HOST` contains the hostname to bind the application to.
7. `PORT` contains the port to bind the application to.
8. `DATA_DIR` contains the directory to store the data in.

When the application starts, it will use `python-dotenv` to set the environment variables listed above. The application then reads the required environment variables and loads them into the application.

To generate a secure value for `JWT_SECRET_KEY`, use the following command:

```bash
openssl rand -hex 32
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
docker run -p 8000:8000 --name todo-fastapi -e JWT_SECRET_KEY=secret -e ALGORITHM=HS256 -e ACCESS_TOKEN_EXPIRE_MINUTES=30 -e ENABLE_REGISTRATIONS=1 -e  RELOAD=0 -e HOST=0.0.0.0 -e PORT=8000 -v ./data:/code/data nickshanks347/todo-fastapi:latest
```

**Again, be sure to use a secure value for `JWT_SECRET_KEY`.**

### Building Docker image

If you want to build the image locally, use the included Dockerfile:

```bash
docker build -t todo-fastapi .
```
