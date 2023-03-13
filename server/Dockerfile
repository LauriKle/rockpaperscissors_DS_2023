FROM python:3.8

WORKDIR /app

COPY server.py .

RUN pip install mysql-connector-python
RUN pip install socket

EXPOSE 8000

CMD [ "python", "./server.py" ]