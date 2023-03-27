import redis
import os
import requests
import shutil
import json
from handle_core import handle_core
from time import sleep

REDIS_URL = os.environ.get('REDIS_URL')
CHANNEL = "pdf-to-handle"
TOKEN = os.environ.get("STATIC_TOKEN")
print(f"TOKEN : {TOKEN}")

def redis_db():
    db = redis.Redis.from_url(REDIS_URL)
    db.ping()
    return db

def redis_queue_pop(db):
    _, message_json = db.brpop(CHANNEL)
    return json.loads(message_json.decode("utf-8"))

def getFile(name):
    url="http://server:5000/uploads/"+name
    res = requests.get(url, headers={'Authorization': f"Bearer {TOKEN}"}, stream=True)
    if res.status_code == 200:
        save_file(name, res.raw)
    else:
        print('Image Couldn\'t be retrieved')

def save_file(name, raw):
    with open(f"app/data/docs/{name}",'wb') as f:
            shutil.copyfileobj(raw, f)
            print('Image sucessfully Downloaded: ',name)

def process_message(obj_message):
    utf_names=obj_message["originalNames"]
    for name in utf_names:
        print(f"name = > {name}", flush=True)
        getFile(name)
    print("it'finished ! ", flush=True)

def main():
    db = redis_db()
    db_publish = redis_db()
    while True:
        message_json = redis_queue_pop(db) 
        process_message(message_json)
        handle_core(db_publish, message_json["date"])
        for i in range(4):
            db_publish.publish('handling_process',json.dumps([i,4]))
            sleep(1)

if __name__ == '__main__':
    main()

