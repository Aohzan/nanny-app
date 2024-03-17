FROM python:3.12-slim-bookworm

EXPOSE 5000

WORKDIR /src
COPY . /src

COPY requirements.txt /
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r /requirements.txt

RUN pybabel compile -d app/translations
