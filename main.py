import telegram

from telegram.ext import Updater, CommandHandler

import genshinstats as gs

# Replace with your own Telegram bot token

TOKEN = '6050800278:AAEDTN1TAGtavX8r1G3Zq0wF5Vqc0AwD0p0'

# Initialize the Telegram bot

bot = telegram.Bot(token=TOKEN)

# Define the command handler for the /stats command

def stats(update, context):

    # Get the player's UID from the command argument

    uid = context.args[0]

    

    # Get the player's stats using the genshinstats library

    player = gs.PlayerStats(uid)

    

    # Format the stats as a string

    stats_str = f"Stats for player {uid}:\n\n"

    stats_str += f"Adventure Rank: {player.get('stats', 'level')}\n"

    stats_str += f"Total Playtime: {player.get('stats', 'play_time')} hours\n"

    stats_str += f"Anemoculi found: {player.get('world_exploration', 'anemoculus')}\n"

    stats_str += f"Geoculi found: {player.get('world_exploration', 'geoculus')}\n"

    

    # Send the stats to the user

    update.message.reply_text(stats_str)

# Initialize the Telegram bot updater and dispatcher

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

# Add the /stats command handler to the dispatcher

dispatcher.add_handler(CommandHandler('stats', stats))

# Start the Telegram bot

updater.start_polling()

# Keep the bot running

updater.idle()



