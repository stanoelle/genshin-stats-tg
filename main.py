import requests

import json

import logging

from telegram import Update

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace YOUR_BOT_TOKEN with your actual bot token obtained from BotFather

TOKEN = '6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A'
# Replace YOUR_API_KEY with the actual API key obtained from Genshin Impact Gamepedia API

API_KEY = None

# Enable logging

logging.basicConfig(

    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:

    """Send a message when the command /start is issued."""

    update.message.reply_text('Hi! Send me the name of a Genshin Impact character to get information on their uses.')

def character_info(update: Update, context: CallbackContext) -> None:

    """Search for character information and send it to the user."""

    character_name = update.message.text

    # Call the API to search for the character

    url = f'https://genshin-impact.fandom.com/api.php?action=parse&page={character_name}&format=json'

    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = json.loads(response.text)

        try:

            # Extract the section containing the character uses

            section = data['parse']['sections'][1]

            section_title = section['line']

            section_text = section['text']

            # Send the information to the user

            update.message.reply_text(f'{section_title}\n\n{section_text}')

        except:

            logger.exception(f'Error retrieving information for {character_name}')

            update.message.reply_text(f'Sorry, I could not find any information on {character_name}.')

    else:

        logger.warning(f'Status code {response.status_code} received when retrieving information for {character_name}')

        update.message.reply_text('Sorry, something went wrong. Please try again later.')

def error_handler(update: Update, context: CallbackContext) -> None:

    """Log any uncaught exceptions."""

    logger.exception(f'Unhandled exception: {context.error}')

def main() -> None:

    """Start the bot."""

    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))

    updater.dispatcher.add_handler(CommandHandler("character_info", character_info))

    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, character_info))

    updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

