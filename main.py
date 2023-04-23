import requests

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

        data = response.json()

        try:

            # Extract the character information

            name = data['name']

            vision = data['vision']

            weapon_type = data['weapon']

            rarity = data['rarity']

            description = data['description']

            # Send the information to the user

            message = f'{name}\n\nVision: {vision}\nWeapon Type: {weapon_type}\nRarity: {rarity}\n\n{description}'

            update.message.reply_text(message)

        except:

            update.message.reply_text(f'Sorry, I could not find any information on {character_name.title()}.')

    else:

        update.message.reply_text(f'Sorry, I could not find any information on {character_name.title()}.')

def error_handler(update: Update, context: CallbackContext) -> None:

    """Log the error and send a message to the user."""

    logger.warning(f'Update {update} caused error {context.error}')

    update.message.reply_text('Sorry, something went wrong. Please try again later.')

def main() -> None:

    """Start the bot."""

    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))

    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, character_info))

    updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

