from collections import namedtuple

Lesson = namedtuple("Lesson", "date auditorium classNumber teacher type name")
StudentGroup = namedtuple("StudentGroup", "groupName pvgusGroupId")

GroupChat = namedtuple("GroupChatSpec", "tgChatId groupName")
GroupDisciplineChat = namedtuple("GroupDisciplineChatSpec", "tgChatId groupName disciplineName")
TeacherChat = namedtuple("TeacherChatSpec", "tgChatId teacherName")
