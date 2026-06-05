import os

from telethon import TelegramClient

from telegram_stalk.config import load_config
from telegram_stalk.logger import ActivityLogger
from telegram_stalk.message_monitor import register_message_monitor
from telegram_stalk.paths import prepare_target_paths
from telegram_stalk.presence_monitor import PresenceMonitor
from telegram_stalk.story_monitor import register_story_monitor


try:
    config = load_config()
except RuntimeError as error:
    print(error)
    exit(1)

client = TelegramClient(config.session_name, config.api_id, config.api_hash)

async def main():
    target_username = input("Enter the user's username (example, @username):").strip()
    os.system('cls' if os.name == 'nt' else 'clear')

    paths = prepare_target_paths(target_username)
    logger = ActivityLogger(paths.log_file)
    target_entity = await client.get_entity(target_username)
    target_user_id = target_entity.id

    print(f"[*] Monitoring of messages, presence and stories from {target_username}...")
    print("[*] To stop the script, press Ctrl+C\n")

    register_message_monitor(client, target_username, paths, logger)
    presence_monitor = PresenceMonitor(client, target_user_id, logger)
    presence_monitor.register()
    register_story_monitor(client, target_user_id, logger)

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.start()
    client.loop.run_until_complete(main())
