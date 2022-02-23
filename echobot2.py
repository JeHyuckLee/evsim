#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import sqlite3

# Connect to SQLite DB
#conn = sqlite3.connect("chat.db")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

'''
conn = sqlite3.connect("chat.db")
with conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE \
             chat_msg(id integer primary key autoincrement, \
                      chat_id integer not null,\
                      msg text not null);")
    
    conn.commit()
'''

# cur.execute("INSERT INTO customer(name, category, region)\
#             VALUES ('cbchoi', 1, 'Daejeon');")
# Define a few command handlers. These usually take the two arguments update and
# context.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    print(update.message.chat_id)
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def check(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect("chat.db")

    text = str()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM chat_msg;")

        for row in cur.fetchall():
            text += row[2]
            text += "\n"

        conn.commit()

    update.message.reply_text(text)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""

    conn = sqlite3.connect("chat.db")

    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO chat_msg(chat_id, msg)\
             VALUES ({update.message.chat_id},'{update.message.text}');")
        conn.commit()

    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5010687528:AAEKtgIMrmvIOiF9XwkLPzCj29E7Cjt8F-I")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    #updater.bot.send_message(1955979869, "hello")

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("check", check))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
