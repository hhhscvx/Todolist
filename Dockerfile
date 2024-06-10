FROM python:3.10.12

COPY requirements.txt /temp/requirements.txt

RUN apt-get update && apt-get install -y postgresql-client build-essential libpq-dev

RUN pip install -r /temp/requirements.txt

COPY . /todolist
WORKDIR /todolist
EXPOSE 8000