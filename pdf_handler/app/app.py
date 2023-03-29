from utils import redis_db, zip_and_remove_output,missing_folder_handler
import os
import requests
import shutil
import json
from handle_core import handle_core

CHANNEL = "pdf-to-handle"
TOKEN = os.environ.get("STATIC_TOKEN")

missing_folder_handler()

def redis_queue_pop(db):
    _, message_json = db.blpop(CHANNEL)
    return json.loads(message_json.decode("utf-8"))

def getFile(name):
    url="http://server:5000/uploads/"+name
    res = requests.get(url, headers={'Authorization': f"Bearer {TOKEN}"}, stream=True)
    if res.status_code == 200:
        save_file(name, res.raw)
    else:
        print('Image Couldn\'t be retrieved',flush=True)

def postFile():
    url="http://server:5000/upload-result/"
    with open('./app/data/pdf_result.zip', 'rb') as f:
        files = {'file': f.read()}
        values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
        r = requests.post(url, files=files, data=values, headers={'Authorization': f"Bearer {TOKEN}"})
        print(f"==> result upload Status : {r.status_code}",flush=True)

#===============================

def save_file(name, raw):
    with open(f"app/data/docs/{name}",'wb') as f:
            shutil.copyfileobj(raw, f)
            print('Image sucessfully Downloaded: ',name)

def delete_result_file():
    os.remove('./app/data/pdf_result.zip')

def process_message(obj_message):
    utf_names=obj_message["originalNames"]
    for name in utf_names:
        print(f"name = > {name}", flush=True)
        getFile(name)
    print("it'finished ! ", flush=True)

def main():
    db = redis_db()
    while True:
        message_json = redis_queue_pop(db)
        process_message(message_json)
        handle_core(message_json["date"])
        # for i in range(4):
        #     db_publish.publish('handling_process',json.dumps([i,4]))
        #     sleep(1)
        zip_and_remove_output()
        postFile()
        delete_result_file()


if __name__ == '__main__':
    main()

