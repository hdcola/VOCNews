import feedparser
import utils as ut
import requests
from datetime import datetime
from logging_conf import logger
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
from lxml import html

log = logger.getChild(__name__)

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


def get_entry_content(entry):
    url = entry.get("link", None)
    if not url:
        return None
    return get_content(url)


def get_content(url):
    response = requests.get(url)
    log.debug(f"GET {url} {response.status_code}")
    if response.status_code != 200:
        return None
    content = response.text
    return content


def get_readability(content):
    cleaner = Cleaner(
        scripts=True,
        javascript=True,
        comments=True,
        style=True,
        page_structure=False,
    )
    doc = html.fromstring(content)
    cleaned_html = cleaner.clean_html(doc)

    # remove header, footer, aside, socialShare, noscript
    for header in cleaned_html.xpath('//header[@id="mainHeader"]'):
        header.getparent().remove(header)
    for div in cleaned_html.xpath('//div[@class="socialShare"]'):
        div.getparent().remove(div)
    for aside in cleaned_html.xpath('//aside'):
        aside.getparent().remove(aside)
    for footer in cleaned_html.xpath('//footer'):
        footer.getparent().remove(footer)
    for noscript in cleaned_html.xpath('//noscript'):
        noscript.getparent().remove(noscript)

    content = html.tostring(cleaned_html).decode('utf-8')
    return content


def dump_rss(file):
    ut.dump_json(rss, file)


if __name__ == "__main__":
    # fetch_rss()
    # dump_rss("lapresse.json")
    # # get last entry content and save to html
    # entry = get_last_entries()
    # content = get_entry_content(entry)
    # if content:
    #     ut.dump_file(content, "lapresse.html")
    # print("done")

    # read lapresse.html to get content
    content = ut.read_file("lapresse.html")
    text = get_readability(content)
    ut.dump_file(text, "parsed_lapresse.html")
