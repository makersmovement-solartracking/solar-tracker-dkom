FROM arm32v7/python:3.7-alpine


COPY . .

RUN apk update
RUN apk upgrade

RUN apk add python py-pip openssl ca-certificates py-openssl wget
RUN apk add --virtual build-dependencies libffi-dev openssl-dev python3-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && apk del build-dependencies

WORKDIR rasp/

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["python3", "run.py"]
