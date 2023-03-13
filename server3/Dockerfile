FROM python:3.8

ADD server.py .

RUN pip install mysql-connector-python

CMD [ "python","-u","server.py","8002"]