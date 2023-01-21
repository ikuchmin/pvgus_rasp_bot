from tinydb import TinyDB, Query

from tg_bot.marshal import serialize, deserialize
import ydb


global db


def get_db():
    global db
    db = TinyDB('tmp/chat_db.json')
    return db


def create_chat(tg_chat):
    db = get_db()
    Chat = Query()

    db.upsert(serialize(tg_chat), Chat.chat_id == tg_chat.tg_chat_id)


def find_chat(chat_id):
    db = get_db()
    Chat = Query()

    chats_raw = db.search(Chat.chat_id == chat_id)
    if len(chats_raw) == 0:
        return None

    chat_raw = chats_raw[0]

    return deserialize(chat_raw)


def find_all_chats():
    db = get_db()
    chats_raw = db.all()

    return [deserialize(chat_raw) for chat_raw in chats_raw]

