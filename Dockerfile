FROM python:3.8

LABEL version="1.0"
LABEL maintainer="Ian Ansell"


RUN apt-get update   
RUN apt-get install --no-install-recommends --no-install-suggests -y curl 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* 

WORKDIR /cjfeedback

COPY . /cjfeedback

CMD bin/bash