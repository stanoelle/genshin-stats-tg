import requests

from telegram import Update

from telegram.ext import Updater, CommandHandler, MessageHandler, filters

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Genshin Impact character info bot! Type /search followed by the character name to retrieve their information.")

def search(update, context):

    char_name = ' '.join(context.args)

    url = f'https://api.genshin.dev/characters/{char_name}'

    response = requests.get(url)

    if response.status_code == 200:

        char_data = response.json()

        info = f"Info for {char_data['name']}:\n\nElement: {char_data['element']} \nWeapon: {char_data['weapon']}\nDescription: {char_data['description']}"

        context.bot.send_message(chat_id=update.effective_chat.id, text=info)

    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Character not found. Please check the spelling and try again.")

def main():

    updater = Updater('6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A', use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('search', search))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

