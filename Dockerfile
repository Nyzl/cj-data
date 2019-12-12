FROM python:3.8

LABEL version="1.0"
LABEL maintainer="Ian Ansell"


#RUN apt-get update -y   
#RUN apt-get install --no-install-recommends --no-install-suggests -y curl 
#RUN apt-get clean && rm -rf /var/lib/apt/lists/* 

RUN pip install --upgrade pip

COPY . /cj-data

WORKDIR /cj-data

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 444 src/*.py
RUN chmod 444 requirements.txt

ENV gcp_project customerjourney-214813
ENV bq_dataset IanTest
ENV advisernet_ga ga:91978884
ENV public_ga ga:93356290
ENV all_ga ga:77768373


ENV PORT 8080

#CMD /bin/bash
CMD python src/controller.py