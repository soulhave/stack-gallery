FROM python:2.7
MAINTAINER Marcus Lacerda "marcus.lacerda@gmail.com"

RUN apt-get update
RUN apt-get install -y python-pip curl

RUN mkdir /app
RUN chmod +x /app

ADD app /app

RUN pip install flask
RUN pip install requests
RUN pip install elasticsearch
RUN pip install httplib2
RUN pip install PyJWT

WORKDIR /app
# -r is not working -> RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run.py"]