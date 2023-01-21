from collections import namedtuple

TgChat = namedtuple("TgChat", "tgChatId spec")
TgGroupChatSpec = namedtuple("TgGroupChatSpec", "groupName")
TgGroupDisciplineChatSpec = namedtuple("TgGroupDisciplineChatSpec", "groupName disciplineName")
TgTeacherChatSpec = namedtuple("TgTeacherChatSpec", "teacherName")