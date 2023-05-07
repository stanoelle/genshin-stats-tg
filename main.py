import telegram

from telegram.ext import Updater, CommandHandler

import genshinstats as gs

import json

import requests

# Replace with your own Telegram bot token

TOKEN = '6050800278:AAEDTN1TAGtavX8r1G3Zq0wF5Vqc0AwD0p0'

# Initialize the Telegram bot

bot = telegram.Bot(token=TOKEN)

# Define the command handler for the /start command

def start(update, context):

    update.message.reply_text('Welcome to the Genshin Impact bot! Use the /char command followed by a character name, or the /weapon command followed by a weapon name to get stats and images.')

# Define the command handler for the /char command

def char(update, context):

    # Check if the command has an argument

    if not context.args:

        update.message.reply_text('Please enter a character name after the /char command.')

        return

    

    # Get the character name from the command argument

    char_name = ' '.join(context.args)

    

    # Get the character stats using the genshinstats library

    try:

        char_data = gs.get_char_data(char_name)

    except gs.errors.GenshinStatsException:

        update.message.reply_text(f"Could not find character {char_name}. Please check the spelling and try again.")

        return

    

    # Get the character image URL

    char_image_url = char_data['image']

    

    # Download the character image

    response = requests.get(char_image_url)

    with open('char_image.jpg', 'wb') as f:

        f.write(response.content)

    

    # Format the character stats as a string

    char_str = f"Stats for character {char_name}:\n\n"

    char_str += f"Element: {char_data['element']}\n"

    char_str += f"Weapon Type: {char_data['weapon']}\n"

    char_str += f"Rarity: {char_data['rarity']}\n"

    char_str += f"Base ATK: {char_data['base_atk']}\n"

    char_str += f"Base HP: {char_data['base_hp']}\n"

    

    # Send the character stats and image to the user

    update.message.reply_photo(photo=open('char_image.jpg', 'rb'))

    update.message.reply_text(char_str)

# Define the command handler for the /weapon command

def weapon(update, context):

    # Check if the command has an argument

    if not context.args:

        update.message.reply_text('Please enter a weapon name after the /weapon command.')

        return

    

    # Get the weapon name from the command argument

    weapon_name = ' '.join(context.args)

    

    # Get the weapon stats using the genshinstats library

    try:

        weapon_data = gs.get_weapon_data(weapon_name)

    except gs.errors.GenshinStatsException:

        update.message.reply_text(f"Could not find weapon {weapon_name}. Please check the spelling and try again.")

        return

    

    # Get the weapon image URL

    weapon_image_url = weapon_data['image']

    

    # Download the weapon image

    response = requests.get(weapon_image_url)

    with open('weapon_image.jpg', 'wb') as f:

        f.write(response.content)

    

    # Format the weapon stats as a string

    weapon_str = f"Stats for weapon {weapon_name}:\n\n"

    weapon_str += f"Weapon Type: {weapon_data['type']}\n"

    weapon_str += f"Rarity: {weapon_data['rarity']}\n"

    weapon_str += f"Base ATK: {weapon_data['base_atk']}\n"

    weapon_str += f"Secondary Stat: {weapon_data['secondary_stat']}\n"

    weapon_str += f"Passive Ability: {weapon_data['passive_name']}\n"

    

    # Send the weapon stats and image to the user

    update.message.reply_photo(photo=open('weapon_image.jpg', 'rb'))

    update.message.reply_text(weapon_str)

# Initialize the Telegram bot updater and dispatcher

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

# Add the /start, /char, and /weapon command handlers to the dispatcher

dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(CommandHandler('char', char))

dispatcher.add_handler(CommandHandler('weapon', weapon))

# Start the Telegram bot

updater.start_polling()

# Keep the bot running

updater.idle()
