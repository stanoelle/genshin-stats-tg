import telegram

import requests

import json

from telegram.ext import Updater, CommandHandler

TOKEN = '6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A'

def start(update, context):

    """Send a message when the command /start is issued."""

    update.message.reply_text('Hi! Welcome to Genshin Impact Character Usage bot. Enter the name of a character to see their usage statistics.')

def get_character_info(character_name):

    """Retrieve character information from the Genshin Impact API."""

    url = f'https://api.genshin.dev/characters/{character_name}'

    response = requests.get(url)

    character_info = json.loads(response.text)

    return character_info

def get_character_usage(character_info):

    """Retrieve character usage statistics from the character information."""

    stats = character_info['stats']

    usage = stats['usage']

    return usage

def character_usage(update, context):

    """Retrieve and display the usage statistics of the requested character."""

    character_name = ' '.join(context.args).title()

    character_info = get_character_info(character_name)

    if 'message' in character_info:

        update.message.reply_text(f"Sorry, I couldn't find any information on {character_name}.")

    else:

        usage = get_character_usage(character_info)

        update.message.reply_text(f"Usage statistics for {character_name}:\n\n{usage}")

def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("usage", character_usage))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

