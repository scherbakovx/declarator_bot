# -*- coding: utf-8 -*-
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ChatAction
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler

from functools import wraps

from utils import validate_request, build_menu
from network import make_request_for_search, make_request_for_person

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '606272084:AAEyMyKaioythxTGakMpUvO4YmnHUgbc0UU'
REQUEST_KWARGS = {
    'proxy_url': 'socks5://holdtherope.ru:1080',
    # # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'proxy-user',
        'password': 'xo2Qa6Pgxhq6Fu6',
    }
}

updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher


# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#send-a-chat-action
def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        chat_id = None
        try:
            chat_id = update.message.chat_id
        except:
            chat_id = update.callback_query.message.chat.id
        bot.send_chat_action(chat_id=chat_id,
                             action=ChatAction.TYPING)
        func(bot, update, **kwargs)

    return command_func


def start(bot, update):
    """
    Function for handling /start-command
    """
    bot.send_message(chat_id=update.message.chat_id,
                     text="*написать возможности этого бота*")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


@send_typing_action
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
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=remove_special_keyboard)
        else:
            button_list = []
            for person in result:
                button_list.append(InlineKeyboardButton(
                    person['text'], callback_data=person['id']))

            reply_markup = InlineKeyboardMarkup(
                build_menu(button_list, n_cols=1))
            bot.send_message(
                chat_id=update.message.chat_id, text="Выберите человека:", reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Неверный формат запроса.',
                         reply_markup=remove_special_keyboard)


text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(text_handler)


@send_typing_action
def callback(bot, update):
    remove_special_keyboard = ReplyKeyboardRemove()
    person_id = int(update.callback_query.data)

    amount, result = make_request_for_person(person_id)

    bot.send_message(chat_id=update.callback_query.message.chat.id,
                     text=result,
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=remove_special_keyboard)


callback_handler = CallbackQueryHandler(callback)
dispatcher.add_handler(callback_handler)

updater.start_polling()
