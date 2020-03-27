#!/bin/bash

FROM ubuntu:16.04
MAINTAINER hyj2508 <hyj2508@smartx.kr>

RUN apt-get update

RUN apt-get install -y python3 
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install paramiko

ADD removememory.py  /tmp/removememory.py

CMD ["/usr/bin/python3", "/tmp/removememory.py"]

