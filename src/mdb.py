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


def get_last_rss(name: str) -> Dict[str, Any]:
    """
    Get the last RSS feed entry for a given source name.

    Args:
        name: Name of the RSS feed source

    Returns:
        Dictionary containing the last RSS feed entry
    """
    log.debug(f"Getting last RSS entry for source: {name}")
    return collection.find_one({"name": name})


def save_rss(rss: Dict[str, Any]) -> Any:
    """
    Save the RSS feed data for a given source name.

    Args:
        name: Name of the RSS feed source
        rss: Dictionary containing the RSS feed data

    Returns:
        InsertOneResult object containing the inserted_id
    """
    name = rss["name"]
    log.debug(f"Saving RSS feed for source: {name}")

    return collection.replace_one(
        {"name": name},  # search criteria
        rss,  # replacement document
        upsert=True  # if document not found, insert it
    )
