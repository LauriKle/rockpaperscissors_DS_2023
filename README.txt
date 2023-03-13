Make sure you have Docker installed.

First of all, create a network called my_network:
docker network create my_network

To start the database:
Navigate to the directory db
docker build -t  mymysql .  
docker run -d -p 3306:3306 --name sqlhost --network my_network mymysql

To start the load balancer:
navigate to the directory balancer
docker build -t myloadbalancer .
docker run --name balancer1 -d -p 8888:8888 --network my_network myloadbalancer

To start a server instance:
docker build -t myserver .
docker run --name server1 -d -p 8000:8000 --network my_network myserver

Then run client.py.