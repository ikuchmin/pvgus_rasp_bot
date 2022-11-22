import locale
from tg_bot import discipline_bot, group_bot

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

def handler(event, context):
    print(event)

    group_name = event['params']['group_name']

    print("Group name: " + group_name)

    discipline_name = event['params'].get('discipline_name', None)

    print("Discipline name: " + str(discipline_name))

    if discipline_name:
        return discipline_bot.handler(event, context)

    return group_bot.handler(event, context)