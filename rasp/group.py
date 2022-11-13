from datetime import date, timedelta, datetime

import pvgus_site.pvgus_rasp as pvgus_rasp


def load_lessons_by_group_name(group_name, from_date, end_date):
    student_group = pvgus_rasp.load_student_group(group_name)
    return pvgus_rasp.load_lessons(student_group, from_date, end_date)

def now(student_group_name, curr_datetime=datetime.now()):
    lessons = today(student_group_name, curr_datetime.date())
    return [l for l in lessons if (l.classNumber.firstStartTime <= curr_datetime.time() <= l.classNumber.secondEndTime)]

def today(student_group_name, curr_date=date.today()):
    return load_lessons_by_group_name(student_group_name, curr_date, curr_date)


def tomorrow(student_group_name, curr_date=date.today()):
    tomorrow = curr_date + timedelta(days=31)
    return load_lessons_by_group_name(student_group_name, tomorrow, tomorrow)


def week(student_group_name, curr_date=date.today()):
    start_week = curr_date - timedelta(days=curr_date.weekday())
    end_week = start_week + timedelta(days=6)
    return load_lessons_by_group_name(student_group_name, start_week, end_week)


def month(student_group_name, curr_date=date.today()):
    start_month = curr_date.replace(day=1)
    end_month = start_month + timedelta(days=31)
    return load_lessons_by_group_name(student_group_name, start_month, end_month)

def two_month(student_group_name, curr_date=date.today()):
    start_month = curr_date.replace(day=1)
    end_month = start_month + timedelta(days=62)
    return load_lessons_by_group_name(student_group_name, start_month, end_month)
