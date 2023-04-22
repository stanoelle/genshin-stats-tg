import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Genshin Impact stats bot! Type /search followed by the player name to retrieve their stats.")

def search(update, context):
    player_name = ' '.join(context.args)
    url = f'https://api.genshin.dev/players/{player_name}'
    response = requests.get(url)
    if response.status_code == 200:
        player_data = response.json()
        stats = f"Stats for {player_data['username']}:\n\nAdventure Rank: {player_data['stats']['generalStats']['highestCharacterLevel']} \nAnemoculus found: {player_data['stats']['anemoculus']['anemoculiFound']} \nGeoculus found: {player_data['stats']['geoculus']['geoculiFound']}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=stats)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Player not found. Please check the spelling and try again.")

def main():
    updater = Updater('YOUR_TELEGRAM_BOT_TOKEN', use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('search', search))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
