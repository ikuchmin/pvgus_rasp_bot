from collections import namedtuple
from datetime import time

LessonPlace = namedtuple("LessonPlace", "number firstStartTime firstEndTime secondStartTime secondEndTime")
lesson_places = {"1": LessonPlace(1, time(8, 30), time(9,15), time(9, 20), time(10, 5)),
                 "2": LessonPlace(2, time(10, 15), time(11, 00), time(11, 5), time(11, 50)),
                 "3": LessonPlace(3, time(12, 35), time(13, 20), time(13, 25), time(14, 10)),
                 "4": LessonPlace(4, time(14, 20), time(15, 5), time(15, 10), time(15, 55)),
                 "5": LessonPlace(5, time(16, 5), time(16, 50), time(16, 55), time(17,35)),
                 "6": LessonPlace(6, time(17, 45), time(18, 30), time(18, 35), time(19, 20)),
                 "7": LessonPlace(7, time(19, 30), time(20, 15), time(20, 20), time(21, 5))}