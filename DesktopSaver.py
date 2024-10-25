  import os
import asyncio
import telegram
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BOT_TOKEN = "your_bot_token_here"
ADMIN_CHAT_ID = "your_admin_chat_id_here"

bot = telegram.Bot(token=BOT_TOKEN)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class DesktopHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            asyncio.run_coroutine_threadsafe(self.send_file(event.src_path), loop)

    async def send_file(self, file_path):
        retry_count = 5
        for attempt in range(retry_count):
            try:
                if os.path.getsize(file_path) == 0:
                    print(f"File is empty, skipping: {file_path}")
                    return

                with open(file_path, 'rb') as document:
                    await bot.send_document(chat_id=ADMIN_CHAT_ID, document=document)
                    print(f"File sent: {file_path}")
                return

            except PermissionError:
                print(f"Permission denied for file: {file_path}. Retrying...")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error sending file: {e}")
                return

async def main():
    path = "Enter_Your_Desktop_Locatio"
    event_handler = DesktopHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    print("The bot is active and monitoring your desktop files.")
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text="The bot is active and monitoring your desktop files.")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Error running the bot: {e}")
