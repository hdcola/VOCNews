from pymongo import MongoClient
from typing import Dict, Any
import utils as ut
from logging_conf import logger

log = logger.getChild(__name__)

uri = ut.ENV.get("MDB_CONNECT", "")
log.debug(f"MongoDB connection URI: {uri}")
client = MongoClient(uri)
db = client["vocnews"]
collection = db["rss"]


def insert_one(data: Dict[str, Any]) -> Any:
    """
    Insert a single document into the collection.

    Args:
        data: Dictionary containing the document to insert

    Returns:
        InsertOneResult object containing the inserted_id
    """
    log.debug(f"Inserting document: {data}")
    return collection.insert_one(data)


def update_one(query: Dict[str, Any]) -> Any:
    """
    Update a single document in the collection.

    Args:
        query: Dictionary containing the update query

    Returns:
        UpdateResult object containing the update result
    """
    log.debug(f"Updating document with query: {query}")
    return collection.update_one(query)


def find_one(query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find a single document in the collection.

    Args:
        query: Dictionary containing the search criteria

    Returns:
        The found document or None if not found
    """
    log.debug(f"Finding document with query: {query}")
    return collection.find_one(query)
