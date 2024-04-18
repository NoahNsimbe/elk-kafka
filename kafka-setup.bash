#!/bin/bash

wget https://dlcdn.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
tar -xzf kafka_2.13-3.7.0.tgz
mv kafka_2.13-3.7.0  kafka
cd kafka

## These two commands should be run in separate windows
# bin/zookeeper-server-start.sh config/zookeeper.properties
# bin/kafka-server-start.sh config/server.properties

bin/kafka-topics.sh --create --topic service-requests-events --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic cleaned-service-requests-events --bootstrap-server localhost:9092

## To consume data
# bin/kafka-console-consumer.sh --topic cleaned-service-requests-events --from-beginning --bootstrap-server localhost:9092

## Other useful commands
# bin/kafka-topics.sh --list --bootstrap-server 34.67.100.196:9092
# bin/kafka-topics.sh --delete --topic cleaned-service-requests-events --bootstrap-server localhost:9092
