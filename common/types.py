from enum import Enum
from collections import namedtuple
from dataclasses import dataclass
import inspect

Lesson = namedtuple("Lesson", "date auditorium classNumber teacher type name")
StudentGroup = namedtuple("StudentGroup", "groupName pvgusGroupId")

ChatType = Enum("ChatType", "GroupChat GroupDisciplineChat TeacherChat")


@dataclass
class Chat:
    tgChatId: int
    type: ChatType
    disciplineName: str = None
    groupName: str = None
    teacherName: str = None

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class StudentGroupChat:
    tgChatId: int
    groupName: str
    type: ChatType = ChatType.GroupChat

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class StudentGroupDisciplineChat:
    tgChatId: int
    groupName: str
    disciplineName: str
    type: ChatType = ChatType.GroupDisciplineChat

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class TeacherChat:
    tgChatId: int
    teacherName: str
    type: ChatType = ChatType.TeacherChat

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })



GroupChat = namedtuple("GroupChatSpec", "tgChatId groupName")
GroupDisciplineChat = namedtuple("GroupDisciplineChatSpec", "tgChatId groupName disciplineName")


