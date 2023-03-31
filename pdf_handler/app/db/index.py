from pymongo import MongoClient
import os


def get_database():
   CONNECTION_STRING = os.getenv("MONGODB_URI")
   print(f"==> mongo  : {CONNECTION_STRING}", flush=True)
   client = MongoClient(CONNECTION_STRING)
   return client['labellevilloise']['log']

def insert_pdf_log(my_collection,pdf_path, user_info, date, state):
   pdf_name=os.path.split(pdf_path)[1]
   data = {
      "pdf_name":pdf_name,
      "user_email":user_info["email"],
      "state": state,
      "date": date
   }
   my_collection.insert_one(data)