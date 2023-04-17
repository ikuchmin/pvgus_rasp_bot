def exclude_tg_command(command, text):
    return text.replace(command, '')


def is_private_chat(chat):
    return chat['type'] == 'private'


def is_admin(chat, chat_member):
    return chat_member['status'] in ['creator', 'administrator']