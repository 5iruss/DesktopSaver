# Desktop Saver Bot

## Description
Desktop Saver Bot is a Telegram bot that monitors your desktop for newly created files and automatically sends them to a designated Telegram chat. It's a convenient way to keep track of important documents, images, and any other files you create on your desktop.

## Features
- Monitors the desktop for new files.
- Sends new files to a specified Telegram chat automatically.
- Handles file permission errors and retries sending files if needed.

## Requirements
- Python 3.8 or higher
- `python-telegram-bot` library
- `watchdog` library

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd DesktopSaverBot
   ```
2. Install the required packages:
   ```bash
   pip install python-telegram-bot watchdog
   ```
3. Update the `BOT_TOKEN` and `ADMIN_CHAT_ID` in the `DesktopSaver.py` file with your own Telegram bot token and chat ID.

## Usage
Run the bot using:
```bash
python DesktopSaver.py
```

The bot will start monitoring your desktop. Once it detects a new file, it will automatically send it to the specified Telegram chat.

## License
This project is licensed under the MIT License.
