# syntax=docker/dockerfile:1
# check=error=true

FROM python:3.14-trixie
ENV PYTHONUNBUFFERED=1

RUN apt-get update

WORKDIR /app

COPY app.py /app

ENTRYPOINT ["python3", "/app/app.py"]

