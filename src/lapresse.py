import feedparser
import utils as ut
from datetime import datetime

name = "lapresse"
rss_url = "https://www.lapresse.ca/actualites/rss"

rss = {
    "name": name,
    "url": rss_url,
    "entries": []
}


def fetch_rss():
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        # "Sat, 23 Nov 2024 14:13:45 -0500" to datatime
        time_format = "%a, %d %b %Y %H:%M:%S %z"
        published = datetime.strptime(entry.published, time_format).isoformat()

        rss["entries"].append({
            "title": entry.title,
            "published": published,
            "summary": entry.summary,
            "link": entry.link,
            "image": entry.links[0].href
        })


def get_last_entries():
    if len(rss["entries"]) == 0:
        return None
    rss["entries"].sort(key=lambda x: x["published"], reverse=False)
    return rss["entries"][-1]


def dump_rss(file):
    ut.dump_json(rss, file)


if __name__ == "__main__":
    fetch_rss()
    dump_rss("lapresse.json")
    print("done")
