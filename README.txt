💬 Random Quote Telegram Bot

Looking for a daily dose of inspiration, wisdom, or humor? This bot sends you random quotes, perfect for brightening your day or sparking new thoughts!
With this bot, you can receive a random quote anytime you need it, whether for motivation, reflection, or just a good laugh.

✅ What does it do?

 • ✨ Sends random quotes on demand
 • 💡 Offers a variety of quote categories, including motivational, philosophical, funny, and more
 • 🌱 Provides a daily quote feature for daily inspiration
 • 📲 Easy-to-use interface to receive quotes directly on Telegram

🔧 Features

✅ Quick and effortless access to a wide range of quotes
✅ Customizable settings for the types of quotes you’d like to receive
✅ Instant delivery of quotes to keep you inspired

📩 Need some inspiration or a quick boost?

Contact me on Telegram, and I’ll set up this bot to deliver your favorite quotes whenever you need them! 🚀

# Instructions for installing and launching a Telegram bot with quotes

This guide will help you install and run a Telegram bot to send random quotes. The instructions are provided for Windows and Linux operating systems.

## Preparation: Getting a bot token

Before you start, you need to create a bot in Telegram and receive its token.:

1. Open Telegram and find the bot @BotFather
2. Send him the command `/newbot`
3. Follow the instructions: enter the name of the bot and its username (must end with "bot")
4. After creating the bot, BotFather will send you a message with the bot token. It looks something like this: `1234567890:ABCDefGhIJKlmnOPQRstUVwxyZ`
5. Copy this token, you will need it later

## Install and run on Windows

### Step 1: Install Python 3.10 (not the latest version for better compatibility)

1. Go to the official Python website: https://www.python.org/downloads/release/python-3106/
2. Scroll down the page and find the "Files" section
3. Download "Windows installer (64-bit)" or "Windows installer (32-bit)" depending on your system (64-bit is suitable in most cases)
4. Run the installer
5. **Important!** Check the box "Add Python 3.10 to PATH" at the beginning of the installation
6. Click "Install Now" (or "Install Now")
7. Wait for the installation to complete and click "Close" (or "Close")

### Step 2: Download and prepare the bot

1. Create a new folder on your computer, for example, "telegram_bot"
2. Copy the file with the bot code (main.py ) to this folder

### Step 3: Install the necessary libraries

1. Press the Win + R keys, type "cmd" and press Enter to open the command prompt
2. Use the 'cd` command to navigate to the folder with the bot, for example:
   ```
   cd C:\Users\ИмяПользователя\Documents\telegram_bot
   ```
3. Install the aiogram library with the command:
   ```
   pip install aiogram==3.0.0 aiohttp
   ```

### Step 4: Setting up the Token

1. Open the main file.py in any text editor (you can use Notepad by right-clicking on the file and selecting "Open with" -> "Notepad")
2. Find the string `API_TOKEN = 'YOUR_BOT_TOKEN'
3. Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather (do not remove the single quotes)
4. Save the file (Ctrl+S)

### Step 5: Launch the Bot

1. At the command prompt, while in the folder with the bot, type the command:
``
   python main.py
   ```
2. You should see the message "Bot is running" or other logs.
3. Now the bot is working! Find it in Telegram by the name you set when creating it, and start chatting.

## Install and run on Linux

### Step 1: Install Python 3.10

1. Open a terminal (Ctrl+Alt+T on most Linux systems)
2. Update the package list:
   ```
   sudo apt update
   ```
3. Install the necessary tools to add the repository.:
   ```
   sudo apt install software-properties-common
   ```
4. Add a repository with Python:
   ```
   sudo add-apt-repository ppa:deadsnakes/ppa
   ```
5. Update the package list again:
   ```
   sudo apt update
   ```
6. Install Python 3.10:
``
   sudo apt install python3.10 python3.10-venv python3-pip
   ```

### Step 2: Create and configure the environment for the bot

1. Create a folder for the bot:
   ```
   mkdir ~/telegram_bot
   cd ~/telegram_bot
   ```
2. Create a virtual environment:
   ```
   python3.10 -m venv venv
   ```
3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
4. Create a file with the code:
``
   nano main.py
``
5. Copy the bot code into the editor that opens
6. Press Ctrl+O to save, then Enter and Ctrl+X to exit the editor.

### Step 3: Install the necessary libraries

1. In the terminal with the activated virtual environment, run:
   ```
   pip install aiogram==3.0.0 aiohttp
   ```

### Step 4: Setting up the Token

1. Open the file with the bot code:
   ```
   nano main.py
   ```
2. Find the string `API_TOKEN = 'YOUR_BOT_TOKEN'
3. Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather (do not remove the single quotes)
4. Save the file (Ctrl+O, then Enter) and exit the editor (Ctrl+X)

### Step 5: Launch the Bot

1. Make sure that you are in the folder with the bot and the virtual environment is activated ("(venv)" should be written at the beginning of the terminal line)
2. Launch the bot:
   ```
   python main.py
   ```
3. You should see the message "The bot is running" or other logs.
4. Now the bot is working! Find it in Telegram by the name you set when creating it, and start chatting.

## How to use the bot

After launching the bot, you can use the following commands in Telegram:

- `/start` - get a welcome message and a list of commands
- `/quote` - get a random quote
- `/author` - select the author of the quote (the bot will ask you to enter the author's name)
- `/refresh` - update the quote database (get new quotes from the API)
- `/cancel` or simply "cancel" - cancel the current operation

## Troubleshooting

### The bot does not run on Windows
- Make sure you have installed Python with the "Add Python to PATH" checkbox
- Try restarting your computer and repeat all the steps
- Make sure that you have entered the correct commands in the command prompt

### The bot does not run on Linux
- Make sure that the virtual environment is activated
- Check if all libraries are installed correctly.
- Check the permissions to run the file: `chmod +x main.py `

### The bot starts, but does not respond in Telegram
- Check if you entered the BotFather token correctly.
- Make sure that the bot is up and running (logs should be visible on the command line or terminal)
- Try restarting the bot

### Error "No module named 'aiogram'"
- Make sure that you have installed all the necessary libraries with the command:
``
  pip install aiogram==3.0.0 aiohttp
  ```

## Additional information

- The bot saves all the quotes to the quotes.db database file
- At the first launch, the bot creates a database with several quotes
- You can add new quotes using the `/refresh` command
