FROM python:3.7

LABEL version="1.0"
LABEL maintainer="Ian Ansell"

RUN pip install --upgrade pip

COPY . /cj-data
WORKDIR /cj-data

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod 444 src/*.py
RUN chmod 444 requirements.txt

ENV gcp_project customerjourney-214813
ENV bq_dataset cj_data
ENV advisernet_ga ga:91978884	
ENV public_ga ga:93356290	
ENV all_ga ga:77768373
ENV PORT 8080

ENV GUNICORN_CMD_ARGS="--timeout 60 --workers 2 --chdir=./src/"


CMD ["gunicorn", "controller:app"]
