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
client.timeout = 30
data_offset = 20
api_limit = 20


# %%
def send_data_to_kafka():
    try:
        offset = api_limit + api_limit
        results = client.get(data_set, limit=api_limit, offset=offset)
        df = pd.DataFrame.from_records(results)

        for _, row in df.iterrows():
            producer.produce(topic, json.dumps(row.to_dict()).encode("utf-8"))

        producer.flush()

        print("Data sent to Kafka topic successfully.")
    except Exception as ex:
        print(ex)


# %%
if __name__ == "__main__":
    print("Started streaming.")
    while True:
        send_data_to_kafka()
        time.sleep(sleep_time)
