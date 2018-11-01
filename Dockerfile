FROM frolvlad/alpine-python3

WORKDIR /app

ADD Globey.py /app

ADD requirements.txt /app

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 Globey.py

