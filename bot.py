# -*- coding: utf-8 -*-
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler

from utils import validate_request, build_menu
from network import make_request_for_search, make_request_for_person

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


def callback(bot, update):
    remove_special_keyboard = ReplyKeyboardRemove()
    person_id = int(update.callback_query.data)

    amount, result = make_request_for_person(person_id)

    bot.send_message(chat_id=update.callback_query.message.chat.id,
                     text=result,
                     reply_markup=remove_special_keyboard)


callback_handler = CallbackQueryHandler(callback)
dispatcher.add_handler(callback_handler)

updater.start_polling()
