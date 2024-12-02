from telegram.ext import ApplicationBuilder
import utils as ut
from logging_conf import logger
from typing import Optional
import asyncio

log = logger.getChild(__name__)
bot_token = ut.ENV.get("TELEGRAM_BOT_TOKEN", "")
chat_ids = ut.ENV.get("TELEGRAM_CHAT_ID", "")

application = ApplicationBuilder().token(token=bot_token).build()


async def send_new(entry: dict, title: str, summary: str, link: str) -> bool:
    """
    Send a Telegram message with an image and formatted caption.

    Args:
        entry: RSS entry containing image URL and original link
        title: Message title
        summary: Message summary
        link: Telegraph article link

    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    if not all([entry.get("image"), title, summary, link]):
        log.error("Missing required parameters")
        return False

    try:
        caption = f"""<a href='{link}'>{title}</a>
{summary}

<b>新闻详情:<a href='{link}'>点击这里</a> | <a href='{entry['link']}'>原文链接</a></b>"""

        chats = chat_ids.split(",")
        log.debug(f"Sending message to chat IDs: {chats}")
        for chat_id in chats:
            await application.bot.send_photo(
                chat_id=chat_id,
                photo=entry["image"],
                caption=caption[:1024],  # Telegram caption length limit
                parse_mode="HTML"
            )
            log.info(f"Message sent successfully: {title}")
        return True

    except Exception as e:
        log.error(f"Failed to send telegram message: {str(e)}")
        return False


async def shutdown():
    """Gracefully shutdown the bot application"""
    try:
        await application.shutdown()
        log.info("Bot application shutdown complete")
    except Exception as e:
        log.error(f"Error during shutdown: {e}")

if __name__ == "__main__":
    async def test():
        entry = {
            "title": "Test Message",
            "image": "https://mobile-img.lpcdn.ca/v2/924x/r3996/8faeb300f65a3207b2311f0f1c7170b6.jpg",
            "link": "https://example.com/original"
        }
        try:
            await send_new(entry, "Test Title", "Test Summary", "https://blog.hdcola.org")
        finally:
            await shutdown()

    asyncio.run(test())
