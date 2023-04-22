import os

import requests

import telegram

from telegram.ext import CommandHandler, Updater

# Replace with your own Telegram bot token

TOKEN = '6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A'

# Define a function to handle the /start command

def start(update, context):

    message = 'Welcome to the Genshin Impact player stats bot! To get started, enter your player name like this: /stats player_name'

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define a function to handle the /stats command

def stats(update, context):

    # Get the player name from the command arguments

    player_name = context.args[0]

    # Retrieve player data from Genshin Impact Official Community API

    url = f"https://api-takumi.mihoyo.com/game_record/app/card/wapi/getGameRecordCard?uid=&server=&nickname={player_name}"

    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",

        "Referer": "https://webstatic-sea.mihoyo.com/",

        "x-rpc-app_version": "2.4.0",

        "DS": "2b7f2c8f-3a79-4a5f-b7d1-92f68e53277a",

    }

    response = requests.get(url, headers=headers)

    player_data = response.json()

    # Check if the player exists

    if player_data.get('retcode') != 0:

        message = f"Sorry, I couldn't find a player with the name {player_name}. Please try again with a valid player name."

        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        return

    # Extract character details from player data

    characters = player_data.get('data', {}).get('avatars', [])

    char_details = ''

    for character in characters:

        char_name = character.get('name')

        char_level = character.get('level')

        char_ascension = character.get('rarity')

        char_details += f"{char_name} (Lv. {char_level}, {char_ascension}⭐)\n"

    # Build the message to send back to the user

    message = f"Player Name: {player_name}\n\n"

    message += f"Adventure Rank: {player_data['data']['level']}\n"

    message += f"Server: {player_data['data']['region']}\n\n"

    message += "Characters:\n"

    message += char_details

    # Send the message back to the user

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Initialize Telegram bot

bot = telegram.Bot(token=TOKEN)

# Initialize the Telegram bot updater and add command handlers

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(CommandHandler('stats', stats))

# Start polling for new messages

updater.start_polling()

updater.idle()

