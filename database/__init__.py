from tinydb import TinyDB, Query


def get_db():
    return TinyDB('tmp/test_db.json')

def create_chat(chat_id):
    db = get_db()
    db.insert({'chat_id': chat_id})