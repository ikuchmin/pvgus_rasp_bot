from tg_bot.types import TgGroupChatSpec, TgGroupDisciplineChatSpec, TgTeacherChatSpec


def serialize(tg_chat):
    spec = tg_chat.spec

    if isinstance(spec, TgGroupChatSpec):
        return {'chat_id': tg_chat.tg_chat_id, 'group_name': spec.group_name, 'type': 'group'}

    if isinstance(spec, TgGroupDisciplineChatSpec):
        return {'chat_id': tg_chat.tg_chat_id, 'group_name': spec.group_name,
                'discipline_name': spec.discipline_name, 'type': 'group_discipline'}

    if isinstance(spec, TgTeacherChatSpec):
        return {'chat_id': tg_chat.tg_chat_id, 'teacher_name': spec.teacher_name, 'type': 'teacher'}


def deserialize(chat_raw):
    if chat_raw['type'] == 'group':
        return TgGroupChatSpec(chat_raw['chat_id'], chat_raw['group_name'])

    if chat_raw['type'] == 'group_discipline':
        return TgGroupDisciplineChatSpec(chat_raw['chat_id'], chat_raw['group_name'], chat_raw['discipline_name'])

    if chat_raw['type'] == 'teacher':
        return TgTeacherChatSpec(chat_raw['chat_id'], chat_raw['teacher_name'])