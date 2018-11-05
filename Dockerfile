FROM frolvlad/alpine-python3

WORKDIR /app

RUN mkdir /storage

ADD requirements.txt /app

RUN apk add py-numpy

RUN pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 Globey.py

ADD Globey.py /app
