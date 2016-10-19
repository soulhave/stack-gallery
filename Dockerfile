FROM python:2.7
MAINTAINER Marcus Lacerda "marcus.lacerda@gmail.com"

RUN apt-get update
RUN apt-get install -y python-pip curl

RUN mkdir /app
RUN chmod +x /app

COPY requirements.txt /app
COPY server.py /app

ADD stack /app/stack

RUN pip install flask
RUN pip install gunicorn

WORKDIR /app
# not work
#RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]