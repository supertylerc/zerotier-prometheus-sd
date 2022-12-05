FROM python:3.11-slim-bullseye as requirements

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11-slim-bullseye

WORKDIR /code
COPY --from=requirements /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./zerotier_prometheus_sd /code/zerotier_prometheus_sd
CMD ["uvicorn", "zerotier_prometheus_sd.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
