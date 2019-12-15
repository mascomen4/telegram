'''import telebot
bot = telebot.TeleBot('1034192214:AAGwl5WUvcTOiISYS2Bx57hyVlIP_ELOcGg')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Привет', 'Пока')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')


bot.polling()
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, datetime

from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

schedule = ["Понедельник\n9:00 - 10:20 Модуль переводчика\n10:30 - 11:50 Модуль переводчика\n12:00 - 13:20 - лекция Алгоритмы и анализ сложности, 700 class\n13:30 - 14:50 - Лекция Физика, 700 кабинет\n15:00 - 16:20 Английский язык",
            "Вторник\n9:00 - 10:20 Практика Дифференциальные уравнения, 547 кабинет \n10:30 - 11:50 Практика Дифференциальные уравнения, 547 кабинет",
            "Среда\n9:00 - 10:20 Лекция Физика, Кравченко Н.Ю., 700 кабинет\n10:30 - 11:50 Лекция Теория вероятностей и мат.статистика, Зарядов И.С., 550 кабинет",
            "Четверг\n9:00 - 10:20 Лекция Дифференциальные уравнения, Кубанова А.К, 550 кабинет \n10:30 - 11:50 Практика Теория вероятностей и мат.статистика, 570 кабинет\n12:00 - 13:20 обед\n13:30 - 14:50 Лаба Алгоритмы и анализ сложностей, ДК-6",
            "Пятница\n9:00 - 10:20 Практика Физика, 210 кабинет\n10:30 - 11:50 Практика Теория вероятностей и мат.статистика, 570 кабинет\n12:00 - 13:20 обед\n13:30 - 15:40 Физическая культура, ФОК",
            "Hoozah! Today's nothing",
            "Yeaaah men, have rest today"]


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


    """Add a job to the queue."""
    chat_id = update.message.chat_id
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()
    new_job = context.job_queue.run_daily(alarm, datetime.time(11, 53), context=chat_id)
    context.chat_data['job'] = new_job


def alarm(context):
    """Send the alarm message."""
    date = datetime.datetime.now()
    day_int = int(date.strftime("%w"))
    job = context.job
    context.bot.send_message(job.context, schedule[day_int-1])


def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1034192214:AAGwl5WUvcTOiISYS2Bx57hyVlIP_ELOcGg", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()