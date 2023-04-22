import requests

from telegram import Update, ParseMode

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:

    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to the Genshin Impact stats bot! Type /search followed by the player name to retrieve their stats.")

def search(update: Update, context: CallbackContext) -> None:

    player_name = ' '.join(context.args)

    url = f'https://api.genshin.dev/players/{player_name}'

    response = requests.get(url)

    if response.status_code == 200:

        player_data = response.json()

        stats = f"Stats for {player_data['username']}:\n\nAdventure Rank: {player_data['stats']['generalStats']['highestCharacterLevel']} \nAnemoculus found: {player_data['stats']['anemoculus']['anemoculiFound']} \nGeoculus found: {player_data['stats']['geoculus']['geoculiFound']}"

        context.bot.send_message(chat_id=update.message.chat_id, text=stats)

    else:

        context.bot.send_message(chat_id=update.message.chat_id, text="Player not found. Please check the spelling and try again.")

def main() -> None:

    updater = Updater('6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A', use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('search', search))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

