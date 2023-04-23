import os

import requests
import logging

from telegram.ext import Updater, CommandHandler

def get_character_info(character_name):

    character_name = character_name.title().replace(" ", "_")

    url = f"https://api.genshin.dev/characters/{character_name}"

    response = requests.get(url)

    if response.status_code == 200:

        character_info = response.json()

        message = f"<b>{character_info['name']}</b>\n\n{character_info['description']}\n\nRarity: {character_info['rarity']}\nVision: {character_info['vision']}\nWeapon: {character_info['weapon']}"

        return message

    else:

        return None

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a Genshin Impact bot. Type /help to see a list of available commands.")

def help(update, context):

    help_message = "Here are the available commands:\n\n/character_info [character name] - Get information about a Genshin Impact character."

    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def character_info(update, context):

    try:

        character_name = context.args[0]

    except IndexError:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the name of the character after the command. For example, /character_info Diluc.")

        return

    character_info = get_character_info(character_name)

    if character_info:

        context.bot.send_message(chat_id=update.effective_chat.id, text=character_info, parse_mode='HTML')

    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sorry, I could not find any information on {character_name.title()}. Please make sure the character name is spelled correctly and try again.")

        

def main():

    updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('help', help))

    dispatcher.add_handler(CommandHandler('character_info', character_info))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

