FROM python:3.9-alpine

ENV PATH="/scrpits:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /Python-OC-Lettings-FR
COPY . /Python-OC-Lettings-FR
WORKDIR /Python-OC-Lettings-FR

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]