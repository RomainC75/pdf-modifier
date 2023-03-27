import redis
import os
import requests
import shutil

REDIS_URL = os.environ.get('REDIS_URL')
CHANNEL = "pdf-to-handle"
# TOKEN = os.environ.get("STATIC_TOKEN")
TOKEN = "AZERTY123"
print(f"TOKEN : {TOKEN}")

def redis_db():
    db = redis.Redis.from_url(REDIS_URL)
    db.ping()
    return db

def redis_queue_pop(db):
    # pop from head of the queue (right of the list)
    # the `b` in `brpop` indicates this is a blocking call (waits until an item becomes available)
    _, message_json = db.brpop(CHANNEL)
    return message_json


def process_message(name):
    print(f"name = > {name}", flush=True)
    utf_name=name.decode("utf-8").replace('"',"")
    print(f"utfName = > {utf_name}", flush=True)
    url="http://server:5000/uploads/"+utf_name
    print(f"url : {url}")
    res = requests.get(url, headers={'Authorization': f"Bearer {TOKEN}"}, stream=True)
    print(f"res : {res}")
    if res.status_code == 200:
        with open(utf_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ',utf_name)
    else:
        print('Image Couldn\'t be retrieved')


def main():
    db = redis_db()

    while True:
        message_json = redis_queue_pop(db)  # this blocks until an item is received
        process_message(message_json)


if __name__ == '__main__':
    main()




# print("=====> REDIS_URL : ", REDIS_URL, flush=True)
# redis_client = redis.Redis.from_url(REDIS_URL)

# # subscribe to a channel
# pubsub = redis_client.pubsub()
# pubsub.subscribe('pdf-to-handle')

# # receive messages
# for message in pubsub.listen():
#     print(f"====={message}=====")

#     print(f"{message['data']}",flush=True)