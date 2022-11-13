from datetime import date, datetime

from pvgus_sdo.pvgus_sdo import Discipline
from rasp import group as rasp_group


def next(student_group_name, discipline_name, curr_date=date.today()):
    lessons = rasp_group.two_month(student_group_name, curr_date)
    return [l for l in lessons if (__discipline_name(l) == discipline_name and l.date >= curr_date)]


def now(student_group_name, discipline_name, curr_datetime=datetime.now()):
    lessons = rasp_group.now(student_group_name, curr_datetime)
    return [l for l in lessons if __discipline_name(l) == discipline_name]


def today(student_group_name, discipline_name, curr_date=date.today()):
    lessons = rasp_group.today(student_group_name, curr_date)
    return [l for l in lessons if __discipline_name(l) == discipline_name]


def tomorrow(student_group_name, discipline_name, curr_date=date.today()):
    lessons = rasp_group.tomorrow(student_group_name, curr_date)
    return [l for l in lessons if __discipline_name(l) == discipline_name]


def week(student_group_name, discipline_name, curr_date=date.today()):
    lessons = rasp_group.week(student_group_name, curr_date)
    return [l for l in lessons if __discipline_name(l) == discipline_name]


def month(student_group_name, discipline_name, curr_date=date.today()):
    lessons = rasp_group.month(student_group_name, curr_date)
    return [l for l in lessons if __discipline_name(l) == discipline_name]


def two_month(student_group_name, discipline_name, curr_date=date.today()):
    lessons = rasp_group.two_month(student_group_name, curr_date)
    return [l for l in lessons if __discipline_name(l) == discipline_name]


def __discipline_name(lesson):
    if isinstance(lesson.name, Discipline):
        return lesson.name.name

    return lesson.name
