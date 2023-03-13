FROM python:3.8

WORKDIR /app

COPY balancer.py .

RUN pip install socket
RUN pip install threading

EXPOSE 8888

CMD ["python", "balancer.py"]