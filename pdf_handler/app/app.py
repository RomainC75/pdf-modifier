from utils import redis_db, zip_and_remove_output,missing_folder_handler
import os
import requests
import shutil
import json
from handle_core import handle_core
from db.index import get_database

CHANNEL = "pdf-to-handle"
TOKEN = os.environ.get("STATIC_TOKEN")
RESULT_FILE=os.environ['RESULT_FILE']
DOCS_FOLDER=os.environ['DOCS_FOLDER']

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

def postFile(user_infos):
    print(f'POSTFILE : {user_infos["email"]}')
    url=f'http://server:5000/upload-result/{user_infos["email"]}'
    # with open('./app/data/pdf_result.tar', 'rb') as f:
    with open(RESULT_FILE, 'rb') as f:
        files = {'file': f.read()}
        values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
        r = requests.post(url, files=files, data=values, headers={'Authorization': f"Bearer {TOKEN}"})
        print(f"==> result upload Status : {r.status_code}",flush=True)

#===============================

def save_file(name, raw):
    with open(f"{DOCS_FOLDER}{name}",'wb') as f:
            shutil.copyfileobj(raw, f)
            print('Image sucessfully Downloaded: ',name)

def delete_result_file():
    os.remove(os.environ["RESULT_FILE"])

def process_message(obj_message):
    utf_names=obj_message["originalNames"]
    for name in utf_names:
        print(f"name = > {name}", flush=True)
        getFile(name)
    print("it'finished ! ", flush=True)

def main():
    db = redis_db()
    print("==> WORKER launched !",flush=True)
    while True:
        message_json = redis_queue_pop(db)
        process_message(message_json)
        handle_core(message_json["date"], message_json['user'])
        # print(f'==> USER { message_json["user"] }',flush=True)
        print(f'==> USER { message_json["user"] }',flush=True)
        # for i in range(4):
        #     db_publish.publish('handling_process',json.dumps([i,4]))
        #     sleep(1)
        zip_and_remove_output()
        postFile(message_json["user"])
        delete_result_file()


if __name__ == '__main__':
    main()

