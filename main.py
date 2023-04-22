import requests

import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Define the Telegram bot token and the API base URL

TOKEN = '6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A'

API_BASE_URL = 'https://api.genshin.dev'

# Define the command handler for the /start command

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I am a Genshin Impact player stats bot. Use the /search command to look up a player\'s stats.')

# Define the command handler for the /search command

def search(update, context):

    # Get the player name from the user's message

    player_name = ' '.join(context.args)

    # Make a GET request to the API to get the player's stats

    response = requests.get(f'{API_BASE_URL}/player/{player_name}')

    # Check if the player was found

    if response.status_code == 404:

        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Player "{player_name}" not found.')

        return

    # Parse the response JSON to get the player's stats

    player_stats = response.json()

    # Generate a message with the player's stats

    message = f'Player: {player_stats["name"]}\n\n'

    message += f'Adventure Rank: {player_stats["stats"]["level"]}\n'

    message += f'Anemoculus Found: {player_stats["stats"]["anemoculus_found"]}\n'

    message += f'Geoculus Found: {player_stats["stats"]["geoculus_found"]}\n'

    message += f'Chests Opened: {player_stats["stats"]["chests"]}\n'

    message += f'Active Characters:\n'

    for character in player_stats["stats"]["characters"]:

        message += f'- {character["name"]} (Level {character["level"]}, Constellation {character["constellation"]})\n'

    # Send the message to the user

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define the error handler

def error(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text='An error occurred. Please try again later.')

# Create the Telegram bot and register the handlers

bot = telegram.Bot(token=TOKEN)

updater = Updater(bot.token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(CommandHandler('search', search))

updater.dispatcher.add_error_handler(error)

# Start the bot

updater.start_polling()

updater.idle()
