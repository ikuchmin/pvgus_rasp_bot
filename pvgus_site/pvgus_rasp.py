from datetime import datetime

from common.types import StudentGroup, Lesson
from pvgus.common import lesson_places
from pvgus_sdo import pvgus_sdo

from requests_html import HTMLSession

pvgus_rasp_url = 'https://www.tolgas.ru/services/raspisanie/?id=0'
pvgus_rasp_teacher_url = 'https://www.tolgas.ru/services/raspisanie/?id=1'

pvgus_rasp_date_format = "%d.%m.%Y"

session = HTMLSession()

def load_student_group(group_name):
    r = session.get(pvgus_rasp_url)

    all_student_groups_options = r.html.find('#vr option')
    option_with_internal_group_id = next(iter([opt for opt in all_student_groups_options if opt.text == group_name]), None)
    if (option_with_internal_group_id is None):
        return None

    return StudentGroup(group_name, option_with_internal_group_id.attrs['value'])


def load_lessons(student_group, fromDate, toDate):

    r = session.post(pvgus_rasp_url,
                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                     data=f'rel=0&grp=0&prep=0&audi=0&vr={student_group.pvgusGroupId}&from={fromDate.strftime("%d.%m.%Y")}&to={toDate.strftime("%d.%m.%Y")}&submit_button=%D0%9F%D0%9E%D0%9A%D0%90%D0%97%D0%90%D0%A2%D0%AC')
    rasp_elements = r.html.find('#send .timetable-frame__row')
    # group elements to add semantic, colspan is an anchor for day
    grouped_by_date = []
    curr_group = []
    for e in rasp_elements:
        if ("timetable-frame__row--2" in e.attrs.get("class")):
            if(len(curr_group) != 0):
                grouped_by_date.append(curr_group)
            curr_group = []
            curr_group.append(e)
        else:
            curr_group.append(e)
            
    if(len(curr_group) != 0):
      grouped_by_date.append(curr_group)

    # build lessons objects
    # copy/paste from somewhere SoF
    def divide_chunks(l, n):
        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]

    lessons = []
    
    for g in grouped_by_date[1:]:
        date = datetime.strptime(g[0].find(".text-lead")[0].text, pvgus_rasp_date_format).date()
        for cl in g[1:]:
            subject = cl.find(".timetable-frame-item__title.text-black")[0].text
            orderSubject = cl.find(".timetable-frame-item__number.title-2")[0].text
            whatTodo = cl.find(".timetable-frame-item__type.text-black")[0].text
            whereShouldBeSubject = cl.find(".timetable-frame-item__text.timetable-frame-item__text--1.m-8.text-small p")[0].text
            teacherName = cl.find(".timetable-frame-item__text.timetable-frame-item__text--1.m-8.text-small p")[1].text
            lessons.append(Lesson(date, whereShouldBeSubject, lesson_places[orderSubject],
                                  teacherName, whatTodo, pvgus_sdo.disciplines_with_sdo.get(subject, subject)))

    return lessons