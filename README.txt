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


You need to start at least one server instance to use the system.
To start server instances:

Server1:
navigate to server's directory
docker build -t myserver .
docker run --name server1 -d -p 8000:8000 --network my_network myserver

Server2:
navigate to server2's directory
docker build -t myserver2 .
docker run --name server2 -d -p 8001:8001 --network my_network myserver2

Server3:
navigate to server3's directory
docker build -t myserver3 .
docker run --name server3 -d -p 8002:8002 --network my_network myserver3

The servers are identical in all aspects except for their names and ports. If you want to test a server with an added delay to simulate timing problems, modify the Dockerfile of a client with the amount of seconds to wait as an argument, like: CMD [ "python","-u","server.py","8000","5"]

Then run client.py normally. Multiple clients can be run at the same time.
Use the command "help" to get info on what commands you can use.
