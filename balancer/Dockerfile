FROM python:3.8

WORKDIR /app

COPY balancer.py .

RUN pip install socket threading

EXPOSE 8888

CMD ["python", "balancer.py"]