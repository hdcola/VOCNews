"""
RSS Feed Parser Module

This module handles RSS feed parsing and processing, providing command line interface
for fetching and storing RSS feed data.
"""

import utils as ut
from logging_conf import logger
import asyncio
from telegram_bot import send_new
import mdb as db
import lapresse as lp
import rssutils

log = logger.getChild(__name__)


async def process_entry(entity):
    """Process a single RSS entry"""
    content = lp.get_entry_content(entity)
    text = lp.get_readability(content)
    telegraph_content = lp.prepare_telegraph_content(text)
    translated_text = lp.translate_content(telegraph_content)
    title = lp.translate_text(
        entity["title"],
        source_lang="French",
        target_lang="Simple Chinese"
    )
    summary = lp.translate_text(
        entity["summary"],
        source_lang="French",
        target_lang="Simple Chinese"
    )
    url = lp.create_telegraph_page(title, translated_text)
    log.info(f"Telegraph URL: {url}")

    await send_new(
        entity,
        title,
        summary,
        url
    )


def main() -> None:
    """Main execution function to fetch and store RSS feed data."""
    try:

        newrss = lp.fetch_rss()
        lastrss = db.get_last_rss(lp.NAME)

        entities = rssutils.get_new_entries(newrss, lastrss)
        if entities:
            log.info(f"New entries found: {len(entities)}")
            db.save_rss(newrss)
            for entity in entities:
                log.info(f"Processing: {
                         entity['published']}-{entity['title']} \n {entity['link']} \n {entity['image']}")
                asyncio.run(process_entry(entity))
        else:
            log.info("No new entries found")

    except Exception as e:
        log.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()
