from typing import Optional, Dict
import feedparser
import utils as ut
import requests
from datetime import datetime
from logging_conf import logger
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
from lxml import html
from telegraph import Telegraph
from translate import translate_text
import rssutils

log = logger.getChild(__name__)

# Constants
NAME = "lapresse"
RSS_URL = "https://www.lapresse.ca/actualites/rss"
TELEGRAPH_TOKEN = ut.ENV.get("TELEGRAPH_TOKEN", "")
DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"

telegraph = Telegraph(access_token=TELEGRAPH_TOKEN)


def fetch_rss() -> None:
    """
    Fetches RSS feed entries from LaPresse and stores them in the rss dictionary.
    Each entry contains title, published date, summary, link and image.
    """
    rss = {
        "name": NAME,
        "url": RSS_URL,
        "entries": []
    }

    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        # "Sat, 23 Nov 2024 14:13:45 -0500" to datatime
        published = datetime.strptime(entry.published, DATE_FORMAT).isoformat()

        rss["entries"].append({
            "title": entry.title,
            "published": published,
            "summary": entry.summary,
            "link": entry.link,
            "image": entry.links[0].href
        })
    return rss


def get_entry_content(entry: Dict) -> Optional[str]:
    """
    Retrieves the full content of an article from its entry URL.
    Args:
        entry: RSS feed entry containing the article link
    Returns:
        str: HTML content of the article or None if retrieval fails
    """
    url = entry.get("link", None)
    if not url:
        return None
    return get_content(url)


def get_content(url: str) -> Optional[str]:
    """
    Fetches content from a given URL using requests.
    Args:
        url: The URL to fetch content from
    Returns:
        str: The response content or None if request fails
    """
    try:
        response = requests.get(url, timeout=10)  # Add timeout
        log.debug(f"GET {url} {response.status_code}")
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        log.error(f"Failed to fetch content: {e}")
        return None


def get_readability(content: str) -> str:
    """
    Cleans HTML content by removing unwanted elements and formatting.
    Args:
        content: Raw HTML content
    Returns:
        str: Cleaned HTML content
    """
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
    soup = BeautifulSoup(content, 'lxml')
    return soup.prettify()


def create_telegraph_page(title: str, html_content: str) -> str:
    """
    Creates a Telegraph page with the given title and content.
    Args:
        title: Page title
        html_content: HTML content for the page
    Returns:
        str: URL of the created Telegraph page
    """
    body = prepare_telegraph_content(html_content)

    response = telegraph.create_page(
        title=title,
        html_content=body
    )
    log.debug(f"telegraph.create_page {response['url']}")
    return response["url"]


def prepare_telegraph_content(html_content: str) -> str:
    """
    Prepares HTML content for Telegraph by cleaning and reformatting elements.
    Args:
        html_content: HTML content to prepare
    Returns:
        str: Prepared HTML content
    """
    soup = BeautifulSoup(html_content, 'lxml')

    #  remove div class="badgeCollection"
    for div in soup.find_all('div', class_="badgeCollection"):
        div.decompose()
    for div in soup.find_all('div', class_="author"):
        div.decompose()

    # remove <header> <h1></h1> </header>
    header = soup.find('header')
    if header:
        h1 = header.find('h1')
        if h1:
            h1.decompose()

    # remove elements but keep content
    for element in soup.find_all(['div', 'section', 'article', 'header', 'small', 'source', 'time']):
        element.unwrap()

    # replace h1 to h3
    for h1 in soup.find_all('h1'):
        h1.name = 'h3'

    # replace h2 to h4
    for h2 in soup.find_all('h2'):
        h2.name = 'h4'

    # replace span to b
    for span in soup.find_all('span'):
        span.name = 'b'

    return soup.body.decode_contents()


def translate_content(content: str) -> str:
    """
    Translates text content from French to Simple Chinese.
    Args:
        content: HTML content to translate
    Returns:
        str: Translated HTML content
    """
    try:
        soup = BeautifulSoup(content, 'lxml')
        for text_node in soup.find_all(string=True):
            if text := text_node.strip():
                translated_text = translate_text(
                    text,
                    source_lang="French",
                    target_lang="Simple Chinese"
                )
                log.debug(f"Translated: {text} -> {translated_text}")
                text_node.replace_with(translated_text)
        return soup.prettify()
    except Exception as e:
        log.error(f"Translation error: {e}")
        return content


if __name__ == "__main__":
    try:
        rss = fetch_rss()
        ut.dump_json(rss, "lapresse.json")

        if entry := rssutils.get_last_entries(rss):
            if content := get_entry_content(entry):
                ut.dump_file(content, "lapresse.html")
                text = get_readability(content)
                ut.dump_file(text, "parsed_lapresse.html")
                telegraph_content = prepare_telegraph_content(text)
                ut.dump_file(telegraph_content, "telegraph.html")
                translated_text = translate_content(telegraph_content)
                title = translate_text(
                    entry["title"],
                    source_lang="French",
                    target_lang="Simple Chinese"
                )
                ut.dump_file(translated_text, "translated_telegraph.html")
                url = create_telegraph_page(title, translated_text)
                print(f"Successfully created page: {url}")
    except Exception as e:
        log.error(f"Process failed: {e}")
