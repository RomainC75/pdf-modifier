import os
import redis
import json

REDIS_URL = os.environ.get('REDIS_URL')

def redis_db():
    db = redis.Redis.from_url(REDIS_URL)
    db.ping()
    return db

def publish(db, channel, data):
    db.publish(channel,json.dumps(data))