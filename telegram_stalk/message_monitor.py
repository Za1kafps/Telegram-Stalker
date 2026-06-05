from telethon import events

from .logger import ActivityLogger, format_dt
from .paths import TargetPaths


def register_message_monitor(client, target_username: str, paths: TargetPaths, logger: ActivityLogger) -> None:
    @client.on(events.NewMessage(from_users=target_username))
    async def handler(event):
        try:
            chat = await event.get_chat()
            chat_name = getattr(chat, "title", "Private messages")

            msg_time = format_dt(event.date)
            text = event.raw_text or "<Without text>"
            log_msg = f"[{msg_time}] Message: Chat: {chat_name} | Text: {text}"

            if event.media:
                if event.photo:
                    path = await event.download_media(file=paths.images)
                    log_msg += f" | [Image: {path}]"
                elif event.voice or event.video_note:
                    path = await event.download_media(file=paths.voice)
                    log_msg += f" | [Voice/Circle: {path}]"
                else:
                    path = await event.download_media(file=paths.files)
                    log_msg += f" | [File: {path}]"

            logger.write(log_msg)
        except Exception as error:
            logger.event("Error", f"Error processing the message: {error}")
