FROM frolvlad/alpine-python3

WORKDIR /app

ADD requirements.txt /app

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 Globey.py

ADD Globey.py /app
