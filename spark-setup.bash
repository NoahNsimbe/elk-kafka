#!/bin/bash

## Local setup. Use dataproc for cloud setup
wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
tar -xvf spark-3.5.1-bin-hadoop3.tgz
mv spark-3.5.1-bin-hadoop3 spark
rm spark-3.5.1-bin-hadoop3.tgz

# cd spark
# ./sbin/start-master.sh

echo "Setup complete."