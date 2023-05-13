import requests

import json

from telegram.bot import Bot

from telegram.ext import Updater, CommandHandler

# Get your bot token from https://api.telegram.org/botfather

TOKEN = "YOUR_TOKEN"

# Create a bot

bot = Bot(TOKEN)

# Define a command handler for the /stats command

@bot.command("stats")

def stats(update, context):

    # Get the search query from the user

    query = update.message.text.split()[1]

    # Make a request to the Paimon.moe API with the player's UID

    response = requests.get("https://paimon.moe/api/users/" + query)

    # Check if the request was successful

    if response.status_code == 200:

        # Get the JSON data from the response

        data = json.loads(response.content)

        # Create a message with the stats of the player

        message = "`Name: {}\nUID: {}\nAdventure Rank: {}\nWorld Level: {}\nCreated: {}\n`".format(

            data["name"], data["uid"], data["adventure_rank"], data["world_level"], data["created"]

        )

        # Send the message to the user

        bot.send_message(update.message.chat_id, message)

    else:

        # Send an error message to the user

        bot.send_message(update.message.chat_id, "Error: " + response.status_code)

# Start the bot

updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler("stats", stats))

updater.start_polling()

updater.idle()

