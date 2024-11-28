from telegram.ext import ApplicationBuilder
import utils as ut
from logging_conf import logger

log = logger.getChild(__name__)
bot_token = ut.ENV.get("TELEGRAM_BOT_TOKEN", "")
chat_id = ut.ENV.get("TELEGRAM_CHAT_ID", "")


async def send_new(entry: dict, title: str, summary: str, link: str) -> None:
    """
    Send a Telegram message with an image and formatted caption using latest telegram API.

    Args:
        entry: RSS entry containing image URL
        title: Message title
        summary: Message summary
        link: Telegraph article link
    """
    try:
        application = ApplicationBuilder().token(token=bot_token).build()
        caption = f"{title}\n\n{summary}\n\n{link}"

        await application.bot.send_photo(
            chat_id=chat_id,
            photo=entry["image"],
            caption=caption,
            parse_mode="HTML"
        )
        log.info("Message sent successfully")
        await application.shutdown()
    except Exception as e:
        log.error(f"Failed to send telegram message: {e}")
        raise

if __name__ == "__main__":
    import asyncio

    entry = {
        "title": "Test",
        "image": "https://mobile-img.lpcdn.ca/v2/924x/r3996/8faeb300f65a3207b2311f0f1c7170b6.jpg"
    }
    asyncio.run(send_new(entry, "Test", "Test", "https://blog.hdcola.org"))
