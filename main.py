import locale

from datetime import datetime

import pytz
from pytz import timezone

from rasp import formatting, group

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

group_name='БОЗИоз22'
discipline_name = 'Алгоритмизация и программирование'
# student_group = pvgus_rasp.load_student_group(group_name)
# print(student_group)
# curr_date = date.today()
# start_month = curr_date.replace(day=1)
# end_month = start_month + timedelta(days=31)
# lessons = pvgus_rasp.load_lessons(student_group, start_month, end_month)
# print(lessons)


samara_tz = timezone('Europe/Samara')
dt = datetime.utcfromtimestamp(1668370473).replace(tzinfo=pytz.utc)
print(dt)
dt = dt.astimezone(samara_tz)
# dt = samara_tz.localize(dt)
print(dt.date())

print("a" + str(None))

s = "02.11.2022"
f = "%d.%m.%Y"
out = datetime.strptime(s, f).date()
print(out)
# lessons = discipline.next(group_name, discipline_name)
github_repo = "http://"
print('/now - занятие сейчас\n'
      '/today - рассписание на сегодня\n'
      '/tomorrow - расписание на завтра\n'
      '/week - расписание на текущую неделю\n'
      '/month - расписание на текущий месяц\n'
      '/two_month - расписание на текущий месяц\n'
      '/week_all - расписание на текущую неделю (включая прошедшие)\n'
      '/month_all - расписание на текущий месяц (включая прошедшие)\n'
      '/two_month_all - расписание на текущий месяц\n\n'
      "PR: [GitHub Repo](" + github_repo + ")")
lessons = group.month(group_name)
print(formatting.grouped_by_date(lessons))



