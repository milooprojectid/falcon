import pymongo
import os


class Database:
    def __init__(self):

        if os.environ.get("APP_ENV") == 'LOCAL':
            self.client = pymongo.MongoClient(
                "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
        else:
            db_user = os.environ.get("DB_USER")
            db_password = os.environ.get("DB_PASS")
            db_cluster = os.environ.get("DB_CLUSTER")
            self.client = pymongo.MongoClient(
                f"mongodb+srv://{db_user}:{db_password}@{db_cluster}-kdbqm.mongodb.net/test?retryWrites=true&w=majority")

        self.db = None
        self.collection = None

    def connect_db(self, database):
        try:
            db_list = self.client.list_database_names()
            if database in db_list:
                print(f"🗄️  {database} selected")
                self.db = self.client[database]
            else:
                print('no database such as {} found'.format(database))

        except Exception as e:
            print(e)

    def select_col(self, collection):
        try:
            col_list = self.db.list_collection_names()
            if collection in col_list:
                self.collection = self.db[collection]
                print(f"➡️  {collection} selected")
            else:
                print(f"no collection such as {collection} found")
        except Exception as e:
            print(e)

    def find_last_object(self):
        if self.collection:
            list_col = self.collection.find().sort('_id', -1)

            for i, t in enumerate(list_col):
                if i == 0:
                    last = t
                    print(f"🔥 {last} selected")
                    return last

    def insert_object(self, data):
        last = self.find_last_object()
        last_id = last['_id'] + 1

        data.update({'_id': last_id})

        self.collection.insert_one(data)
        print("💾 saved {}".format(data))

    def find_object(self, key):
        for a in self.collection.find({'key': key}):
            return a['value']

    def find_and_modify(self, key, value):
        self.collection.find_one_and_update(
            {'key': key}, {'$set': {'value': value}})
        print(f"Value of {key} changed to {value}")
