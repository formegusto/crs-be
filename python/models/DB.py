from dbm.dumb import _Database
import json
from bson.objectid import ObjectId
from pymongo import MongoClient as mc
import datetime as dt


class DB:
    def __init__(self):
        with open('python/env.json', 'r') as f:
            env = json.loads(f.read())
        mongo_uri = "mongodb://{}:{}".format(
            env['MONGO_URI'], env['MONGO_PORT'])
        self.conn = mc(mongo_uri).crs
        self.pro_col = self.conn.process

    def find_process(self, id):
        query = {
            "_id": ObjectId(id)
        }
        return self.pro_col.find_one(query)

    def save_new_process(self, id, in_db):
        query = {
            "_id": ObjectId(id)
        }
        newvalues = {
            "$set": in_db
        }
        self.pro_col.update_one(query, newvalues)

    def process_step_update(self, id, step):
        update_time = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        query = {
            "_id": ObjectId(id)
        }
        newvalues = {
            "$set": {
                "step": step,
                "updatedAt": update_time
            }
        }
        self.pro_col.update(query, newvalues)

    def __call__(self):
        return self.conn
