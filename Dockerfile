FROM python:3.7.1-slim-stretch

WORKDIR /app

RUN mkdir /storage

ADD requirements.txt /app

RUN apt update

RUN apt install -y python3-numpy sqlite3

RUN pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 -m Globey

ADD Globey /app/Globey

ADD reactions.ini /app/

ADD helptext.txt /app/

ADD globes.default /app/

ADD .admins /app/

ADD globes /app/globes

ADD schema.sql /app/