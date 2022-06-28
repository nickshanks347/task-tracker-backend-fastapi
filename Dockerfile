FROM python:3.10

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-dev

COPY ./ /code

CMD ["python", "main.py"]