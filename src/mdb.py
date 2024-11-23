from pymongo import MongoClient
import utils as ut
from logging_conf import logger

log = logger.getChild(__name__)

uri = ut.ENV.get("MDB_CONNECT", "")
log.debug(f"uri: {uri}")
client = MongoClient(uri)
db = client["vocnews"]
collection = db["rss"]


def insert_one(data):
    log.debug(f"insert_one: {data}")
    return collection.insert_one(data)


def update_one(data):
    log.debug(f"update_one: {data}")
    return collection.update_one(data)


def find_one(data):
    log.debug(f"find_one: {data}")
    return collection.find_one(data)
