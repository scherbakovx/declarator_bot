import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from utils import validate_request
from network import make_request_for_search

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


def text(bot, update):
    """
    Function for handling text-messages
    """
    remove_special_keyboard = ReplyKeyboardRemove()
    if validate_request(update.message.text):
        amount, result = make_request_for_search(update.message.text)
        if amount == 0 or amount > 25:
            bot.send_message(chat_id=update.message.chat_id,
                            text=result,
                            reply_markup=remove_special_keyboard)
        elif amount == 1:
            bot.send_message(chat_id=update.message.chat_id,
                            text=result,
                            reply_markup=remove_special_keyboard)
        else:
            # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#build-a-menu-with-buttons
            data = {
                'user_id': update.message.chat_id,
                'time': None # timezone now
                'buttons': [
                    {
                        'button_text': 'office-position 1',
                        'person_id': 1
                    },
                    {
                        'button_text': 'office-position 2',
                        'person_id': 2
                    }
                ]
            }
            custom_keyboard = [['top-left', 'top-right'], ['bottom-left', 'bottom-right']]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard)
            bot.send_message(chat_id=chat_id, text="Custom Keyboard Test", reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Неверный формат запроса.',
                         reply_markup=remove_special_keyboard)


text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(text_handler)

updater.start_polling()
