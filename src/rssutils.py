from typing import Optional, Dict


def get_last_entries(rss) -> Optional[Dict]:
    """
    Returns the most recent entry from the RSS feed.
    Returns None if no entries exist.

    Args:
        rss: Dictionary containing RSS feed entries
    Returns:
        Optional[Dict]: Most recent entry or None if empty
    """
    entries = rss.get("entries", [])
    entries.sort(key=lambda x: x["published"], reverse=False)
    return entries[-1] if entries else None


def get_new_entries(newrss, lastrss) -> Optional[Dict]:
    """
    Compares two RSS feeds and returns entries newer than the latest entry in lastrss.

    Args:
        newrss: Dictionary containing new RSS feed entries
        lastrss: Dictionary containing last RSS feed entries
    Returns:
        Optional[Dict]: New entries or None if no new entries
    """
    if not (last_entry := get_last_entries(lastrss)):
        return newrss["entries"]

    new_entries = [entry for entry in newrss["entries"]
                   if entry["published"] > last_entry["published"]]
    return new_entries if new_entries else None
