import itertools

from pvgus_sdo.pvgus_sdo import Discipline

empty_lessons = 'Лекций и практик в расписании нет'

def without_date(lessons):
    message = '\n'.join(__lesson_without_date(l) for l in lessons)
    return message or empty_lessons

def grouped_by_date(lessons):
    lessons_by_date = [(k, list(g)) for k, g in itertools.groupby(lessons, lambda x: x.date)]

    message = ""
    for (d, ls) in lessons_by_date:
        message += '*' + d.strftime("%d.%m.%Y (%A)") + '*\n' + '\n'.join(__lesson_without_date(l) for l in ls) + '\n\n'

    return message or empty_lessons


def __lesson_without_date(l):
    if isinstance(l.name, Discipline):
        return " | ".join([__lesson_place(l.classNumber), f'[{l.auditorium}]({l.name.blu_button_link})', l.type, f'[{l.name.name}]({l.name.sdo_link})', l.teacher])

    return " | ".join([__lesson_place(l.classNumber), l.auditorium, l.type, str(l.name), l.teacher])



def __lesson_place(lp):
    def format_time(t):
        return t.strftime("%H:%M")

    return f'`{lp.number}-я пара` | `{format_time(lp.firstStartTime)}-{format_time(lp.secondEndTime)}`'
