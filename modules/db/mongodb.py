import pymongo
import os


class MongoDB:
    def __init__(self, connectionString):
        self.client = pymongo.MongoClient(connectionString)
        self.db = None
        self.collection = None

        # if os.environ.get("APP_ENV") == 'LOCAL':
        # else:
        #     db_user = os.environ.get("DB_USER")
        #     db_password = os.environ.get("DB_PASS")
        #     db_cluster = os.environ.get("DB_CLUSTER")
        #     self.client = pymongo.MongoClient(
        #         f"mongodb+srv://{db_user}:{db_password}@{db_cluster}-kdbqm.mongodb.net/test?retryWrites=true&w=majority")

    def connect_db(self, database):
        try:
            db_list = self.client.list_database_names()
            if database in db_list:
                print(f"🗄️  {database} selected")
                self.db = self.client[database]
                return True
            else:
                print(f"{database} not found")
                self.db = self.client[f"{database}"]
                print(f"Database {database} created")

                new_collection = "environment"
                self.collection = self.db[new_collection]
                print(f"Collection {new_collection} created")

        except Exception as e:
            print(e)

    def insert_first_data(self, data: dict):
        data['_id'] = 1
        self.collection.insert_one(data)

    def select_col(self, collection):
        try:
            col_list = self.db.list_collection_names()
            if collection in col_list:
                self.collection = self.db[collection]
                print(f"➡️  {collection} selected")
            else:
                print(f"no collection such as {collection} found")
                self.collection = self.db[collection]
                print(f"Collection {collection} created")
        except Exception as e:
            print(e)

    def find_last_object(self):
        if self.collection:
            list_col = self.collection.find().sort('_id', -1)

            for i, t in enumerate(list_col):
                if i == 0:
                    last = t
                    return last

    def insert_object(self, data):
        last = self.find_last_object()
        last_id = last['_id'] + 1 if last != None else 1

        data.update({'_id': last_id})

        self.collection.insert_one(data)
        print("💾 saved {}".format(data))

    def find_object(self, key):
        for a in self.collection.find({'key': key}):
            return a['value']

    def find_and_modify(self, data):
        self.collection.find_one_and_update(
            {'key': '_id'}, {'$set': data})
        print(f"Data changed to {data}")
