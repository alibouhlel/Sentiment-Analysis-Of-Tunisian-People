#!/bin/bash  
echo "Starting kafka and zookeeper"
sudo kill `sudo lsof -t -i:2181`&sudo docker run -p  2181:2181 -p 9092:9092 -e ADVERTISED_HOST=127.0.0.1  johnnypark/kafka-zookeeper
exit 
