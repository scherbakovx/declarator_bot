import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token='606272084:AAEyMyKaioythxTGakMpUvO4YmnHUgbc0UU')
dispatcher = updater.dispatcher


def start(bot, update):
    """
    Function for handling /start-command
    """
    bot.send_message(chat_id=update.message.chat_id,
                     text="*написать возможности этого бота*")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(bot, update):
    """
    Function for handling text-messages
    """
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
