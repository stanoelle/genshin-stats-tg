import requests

from telegram import Update

from telegram.ext import Updater, CommandHandler, MessageHandler, filters

def start(update):

    update.message.reply_text('Welcome to the Genshin Impact character bot! Type /search followed by the character name to retrieve their info.')
def search(update, context):

    character_name = ' '.join(context.args)

    url = f'https://api.genshin.dev/characters/{character_name}'

    response = requests.get(url)

    if response.status_code == 200:

        character_data = response.json()

        message = f"{character_data['name']}\n\nElement: {character_data['element']} \nWeapon: {character_data['weapon']} \nRarity: {character_data['rarity']} \nDescription: {character_data['description']}"

        update.message.reply_text(message)

    else:

        update.message.reply_text("Character not found. Please check the spelling and try again.")

def main():

    updater = Updater(token="6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A")


    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('search', search))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

