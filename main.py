import os
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

if not API_ID or not API_HASH:
    print("Error: Specify API_ID and API_HASH in the .env file")
    exit(1)
client = TelegramClient('user_session', int(API_ID), API_HASH)

async def main():
    target_username = input("Enter the user's username (example, @username):").strip()
    os.system('cls' if os.name == 'nt' else 'clear')
    clean_username = target_username.replace("@", "")
    print(f"[*] Monitoring of messages from {target_username}...")
    print("[*] To stop the script, press Ctrl+C\n")
    dirs = {
        "images": f"images-{clean_username}",
        "files": f"files-{clean_username}",
        "voice": f"voice-{clean_username}"
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    log_file = f"log-{clean_username}.txt"
    @client.on(events.NewMessage(from_users=target_username))
    async def handler(event):
        try:
            chat = await event.get_chat()
            chat_name = getattr(chat, 'title', 'Private messages')
            
            msg_time = event.date.strftime('%Y-%m-%d %H:%M:%S')
            text = event.raw_text or "<Without text>"

            log_msg = f"[{msg_time}] Chat: {chat_name} | Text: {text}"
            if event.media:
                if event.photo:
                    path = await event.download_media(file=dirs["images"])
                    log_msg += f" | [Image: {path}]"
                elif event.voice or event.video_note:
                    path = await event.download_media(file=dirs["voice"])
                    log_msg += f" | [Voice/Circle: {path}]"
                else:
                    path = await event.download_media(file=dirs["files"])
                    log_msg += f" | [File: {path}]"
            print(log_msg)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_msg + "\n")
                
        except Exception as e:
            print(f"[-] Error processing the message: {e}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.start()
    client.loop.run_until_complete(main())