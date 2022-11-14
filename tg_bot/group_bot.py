import json
from datetime import datetime

import pytz
from pytz import timezone

import telegram
from telegram import Update, Bot
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext import Dispatcher

from common.github import github_repo
from rasp import formatting as rasp_f
from rasp import group as rasp_group
from tg_bot.token import tg_tokens

curr_datetime = datetime.now()
group_name = ""

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Я бот расписания для группы " + group_name + ", вызови /help чтобы узнать список команд.\n"
                                  "PR: " + github_repo,
                             parse_mode=telegram.ParseMode.MARKDOWN)


def now(update: Update, context: CallbackContext):

    lessons = rasp_group.now(group_name, curr_datetime=curr_datetime)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.without_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def today(update: Update, context: CallbackContext):

    lessons = rasp_group.today(group_name, curr_date=curr_datetime.date())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.without_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def tomorrow(update: Update, context: CallbackContext):
    lessons = rasp_group.tomorrow(group_name, curr_date=curr_datetime.date())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.without_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def week(update: Update, context: CallbackContext):
    lessons = rasp_group.week(group_name, curr_date=curr_datetime.date())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def week_all(update: Update, context: CallbackContext):
    lessons = rasp_group.week(group_name, curr_date=curr_datetime.date(), only_future=False)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def month(update: Update, context: CallbackContext):
    lessons = rasp_group.month(group_name, curr_date=curr_datetime.date())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def month_all(update: Update, context: CallbackContext):
    lessons = rasp_group.month(group_name, curr_date=curr_datetime.date(), only_future=False)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def two_month(update: Update, context: CallbackContext):
    lessons = rasp_group.two_month(group_name, curr_date=curr_datetime.date())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def two_month_all(update: Update, context: CallbackContext):
    lessons = rasp_group.two_month(group_name, curr_date=curr_datetime.date(), only_future=False)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='/now - занятие сейчас\n'
                                  '/today - рассписание на сегодня\n'
                                  '/tomorrow - расписание на завтра\n'
                                  '/week - расписание на текущую неделю\n'
                                  '/month - расписание на текущий месяц\n'
                                  '/two_month - расписание на два месяца\n'
                                  '/week_all - расписание на текущую неделю (включая прошедшие)\n'
                                  '/month_all - расписание на текущий месяц (включая прошедшие)\n'
                                  '/two_month_all - расписание на два месяца (включая прошедшие)\n\n'
                                  "PR: " + github_repo)


def handler(event, context):

    global group_name
    group_name = event['params']['group_name']

    bot = Bot(token=tg_tokens[group_name].token)
    dispatcher = Dispatcher(bot, None, use_context=True)

    # register group bot commands
    for (command, handler) in [('start', start),
                               ('now', today),
                               ('today', today),
                               ('tomorrow', tomorrow),
                               ('week', week),
                               ('week_all', week_all),
                               ('month', month),
                               ('month_all', month_all),
                               ('two_month', two_month),
                               ('two_month_all', two_month_all),
                               ('help', help)]:
        h = CommandHandler(command, handler)
        dispatcher.add_handler(h)

    tg_body = json.loads(event["body"])

    global curr_datetime
    curr_datetime = datetime.utcfromtimestamp(tg_body["message"]["date"]).replace(tzinfo=pytz.UTC)

    samara_tz = timezone('Europe/Samara')
    curr_datetime = curr_datetime.astimezone(samara_tz)

    print("Message datetime (SMR): " + str(curr_datetime))

    dispatcher.process_update(Update.de_json(tg_body, bot))

    return {
        'statusCode': 200
    }
