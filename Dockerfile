FROM python:3

ENV PYTHONUNBUFFERED=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip3

RUN pip3 install -r requirements.txt

COPY . /app/

EXPOSE 8000