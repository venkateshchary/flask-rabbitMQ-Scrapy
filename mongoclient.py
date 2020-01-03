from pymongo import MongoClient



def mongoconnection():
    client = MongoClient("localhost",27017)
    db = client.rabbitmqdb
    collection = db['rabbitmqcoll']
    return collection