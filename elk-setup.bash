#!/bin/bash
current_user=$USER

mkdir elk && cd elk

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/logstash/logstash-6.7.1.tar.gz
wget https://dlcdn.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz

tar -xvf elasticsearch-6.7.1.tar.gz
tar -xvf kibana-6.7.1-linux-x86_64.tar.gz
tar -xvf logstash-6.7.1.tar.gz
tar -xzf kafka_2.13-3.7.0.tgz

mv elasticsearch-6.7.1 elastasticsearch
mv kibana-6.7.1-linux-x86_64 kibana
mv logstash-6.7.1 logstash
mv kafka_2.13-3.7.0 kafka

rm elasticsearch-6.7.1.tar.gz
rm kibana-6.7.1-linux-x86_64.tar.gz
rm logstash-6.7.1.tar.gz
rm kafka_2.13-3.7.0.tgz

########## Setup elasticsearch  ##########
# nano /home/$current_user/elk/elastasticsearch/config/elasticsearch.yml
# replace #network.host: 192.168.0.1 with network.host: "0.0.0.0"

########## Setup Kibana ##########
# nano /home/$current_user/elk/kibana/config/kibana.yml
# uncomment server.port: 5601
# replace #server.host:"localhost" with server.host: "0.0.0.0"

sudo apt update -y
sudo apt install default-jdk -y
sudo apt install python3
sudo apt install python3.8-venv

######### Increasing resources ########
# cd /etc 
# sudo sysctl -w vm.max_map_count=100262144

### Staring Kibana, elasticsearch and logstash  #######
# cd /home/$current_user/elk/elastasticsearch && bin/elasticsearch
# cd /home/$current_user/elk/logstash && bin/logstash -f /home/ayepwebsite/elk/logstash.config
# cd /home/$current_user/elk/kibana && bin/kibana
# http://<vm external ip>:5601

echo "Setup complete."
