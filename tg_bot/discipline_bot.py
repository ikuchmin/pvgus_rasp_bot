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
from rasp import discipline as rasp_discipline
from tg_bot.token import tg_tokens

curr_datetime = datetime.now()
group_name = ""
discipline_name = ""

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Я бот расписания для группы " + group_name +
                                  ", вызови /help чтобы узнать список команд.\n"
                                  "PR: " + github_repo,
                             parse_mode=telegram.ParseMode.MARKDOWN)


def now(update: Update, context: CallbackContext):
    lessons = rasp_discipline.now(group_name, discipline_name, curr_datetime=curr_datetime)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.without_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def next(update: Update, context: CallbackContext):
    lessons = rasp_discipline.next(group_name, discipline_name, curr_date=curr_datetime.date())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def today(update: Update, context: CallbackContext):
    lessons = rasp_discipline.today(group_name, discipline_name, curr_date=curr_datetime.date())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.without_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def tomorrow(update: Update, context: CallbackContext):
    lessons = rasp_discipline.tomorrow(group_name, discipline_name, curr_date=curr_datetime.date())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.without_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def week(update: Update, context: CallbackContext):
    lessons = rasp_discipline.week(group_name, discipline_name, curr_date=curr_datetime.date())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def month(update: Update, context: CallbackContext):
    lessons = rasp_discipline.month(group_name, discipline_name, curr_date=curr_datetime.date())

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=rasp_f.grouped_by_date(lessons),
                             parse_mode=telegram.ParseMode.MARKDOWN)


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='/now - занятие сейчас\n'
                                  '/next - будущие занятия\n'
                                  '/today - рассписание на сегодня\n'
                                  '/tomorrow - расписание на завтра\n'
                                  '/week - расписание на текущую неделю\n'
                                  '/month - расписание на текущий месяц\n\n'
                                  "PR: " + github_repo)


def handler(event, context):
    print(event)

    global group_name, discipline_name
    group_name = event['params']['group_name']
    discipline_name = event['params']['discipline_name']

    bot = Bot(token=tg_tokens[group_name + discipline_name].token)
    dispatcher = Dispatcher(bot, None, use_context=True)

    # register group bot commands
    for (command, handler) in [('start', start),
                               ('now', now),
                               ('next', next),
                               ('today', today),
                               ('tomorrow', tomorrow),
                               ('week', week),
                               ('month', month),
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
