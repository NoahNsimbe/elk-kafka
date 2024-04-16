# %%
from confluent_kafka import Producer
import pandas as pd
import json
from sodapy import Socrata
import time

# %%
data_url = "data.cityofnewyork.us"
data_set = "erm2-nwe9"
app_token = "tEeu8oBfckAQMIatiKafE7oeO"
bootstrap_servers = "localhost:9092"
topic = "service-requests-events"
sleep_time = 5

# %%
client = Socrata(data_url, app_token)
producer = Producer({"bootstrap.servers": bootstrap_servers})
client.timeout = 60
offset = 0
api_limit = 100


# %%
def send_data_to_kafka(api_offset):
    try:
        results = client.get(data_set, limit=api_limit, offset=api_offset)
        df = pd.DataFrame.from_records(results)

        for _, row in df.iterrows():
            producer.produce(topic, row.to_json())

        producer.flush()

        print("Data sent to Kafka topic successfully.")
    except Exception as ex:
        print(ex)


# %%
if __name__ == "__main__":
    print("Started streaming.")
    while True:
        send_data_to_kafka(offset)
        time.sleep(5)
        offset = offset + api_limit
