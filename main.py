from datetime import datetime

import pytz
from pytz import timezone

from rasp import formatting, group

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

lessons = group.now(group_name, curr_datetime=datetime(2022, 11, 28, 19, 20, 00))
print(formatting.grouped_by_date(lessons))


