from collections import namedtuple

Discipline = namedtuple("Discipline", "name sdo_link blu_button_link")
disciplines_with_sdo = {"Русский язык и культура речи": Discipline("Русский язык и культура речи",
                                                                   "http://sdo.tolgas.ru/course/view.php?id=11251",
                                                                   "http://sdo.tolgas.ru/mod/bigbluebuttonbn/view.php?id=208325"),
                        "Алгоритмизация и программирование": Discipline("Алгоритмизация и программирование",
                                                                        "http://sdo.tolgas.ru/course/view.php?id=12161",
                                                                        "http://sdo.tolgas.ru/mod/bigbluebuttonbn/view.php?id=195343"),
                        "Математика": Discipline("Математика",
                                                 "http://sdo.tolgas.ru/course/view.php?id=11646",
                                                 "http://sdo.tolgas.ru/mod/bigbluebuttonbn/view.php?id=231374"),
                        "Введение в цифровую культуру": Discipline("Введение в цифровую культуру",
                                                                   "http://sdo.tolgas.ru/course/view.php?id=12164",
                                                                   "http://sdo.tolgas.ru/mod/bigbluebuttonbn/view.php?id=195381"),
                        "Введение в профессию": Discipline("Введение в профессию",
                                                           "http://sdo.tolgas.ru/course/view.php?id=11979",
                                                           "http://sdo.tolgas.ru/mod/bigbluebuttonbn/view.php?id=192747"),
                        "Основы проектной деятельности": Discipline("Основы проектной деятельности",
                                                                    "http://sdo.tolgas.ru/course/view.php?id=12633",
                                                                    "http://sdo.tolgas.ru/mod/bigbluebuttonbn/view.php?id=206611")}
