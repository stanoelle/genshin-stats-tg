import requests
from telegram.ext import Updater, CommandHandler

# Telegram Bot Token
TOKEN = '6050800278:AAEDTN1TAGtavX8r1G3Zq0wF5Vqc0AwD0p0'

# Handler for the /stats command
def stats(update, context):
    # Get the username provided by the user
    username = context.args[0] if len(context.args) > 0 else None
    
    if username:
        # Construct the API URL
        url = f'https://paimon.moe/api/users/{username}'

        try:
            # Send a GET request to the API
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                # Extract the desired player stats
                player_stats = {
                    'Username': data['data']['username'],
                    'Adventure Rank': data['data']['stats']['general']['stats']['active_day_number'],
                    'Achievements': data['data']['stats']['general']['stats']['achievement_number'],
                    'Anemoculi Found': data['data']['stats']['explorations']['anemoculi'],
                    'Geoculi Found': data['data']['stats']['explorations']['geoculi']
                }

                # Generate the stats message
                stats_message = '\n'.join(f'{key}: {value}' for key, value in player_stats.items())
                context.bot.send_message(chat_id=update.effective_chat.id, text=stats_message)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Player not found.')
        except requests.exceptions.RequestException as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text='An error occurred while fetching player stats.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please provide a username.')

# Create an instance of the Updater class and pass your bot token
updater = Updater(token=TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the /stats command handler
dispatcher.add_handler(CommandHandler('stats', stats))

# Start the bot
updater.start_polling()

# Run the bot until it's stopped manually or an exception occurs
updater.idle()
