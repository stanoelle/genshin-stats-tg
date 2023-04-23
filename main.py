import requests

import json

import logging

from telegram import Update

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace YOUR_BOT_TOKEN with your actual bot token obtained from BotFather

TOKEN = '6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A'

def start(update: Update, context: CallbackContext) -> None:

    """Send a message when the command /start is issued."""

    update.message.reply_text('Hi! Send me the name of a Genshin Impact character to get information on their uses.')

def character_info(update: Update, context: CallbackContext) -> None:

    """Search for character information and send it to the user."""

    character_name = update.message.text.lower()

    # Call the API to search for the character

    url = f'https://api.genshin.dev/characters/{character_name}'

    response = requests.get(url)

    if response.status_code == 200:

        data = json.loads(response.text)

        try:

            # Extract the character uses

            uses = data['data']['description']

            # Send the information to the user

            update.message.reply_text(f'{character_name.capitalize()} uses:\n\n{uses}')

        except:

            update.message.reply_text(f'Sorry, I could not find any information on {character_name.capitalize()}.')

    else:

        update.message.reply_text('Sorry, something went wrong. Please try again later.')

def error_handler(update: Update, context: CallbackContext) -> None:

    """Log the error and send a message to the user."""

    logging.warning(f'Update "{update}" caused error "{context.error}"')

    update.message.reply_text('Sorry, something went wrong. Please try again later.')

def main() -> None:

    """Start the bot."""

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))

    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, character_info))

    updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

