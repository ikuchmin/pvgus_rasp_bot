from tinydb import TinyDB, Query

from tg_bot.marshal import serialize, deserialize
from common.types import GroupChat

import os
import ydb


global db

# Create driver in global space.
# driver = ydb.Driver(endpoint=os.getenv('YDB_ENDPOINT'), database=os.getenv('YDB_DATABASE'))
os.environ['GRPC_DNS_RESOLVER'] = 'native'
driver = ydb.Driver(endpoint='grpc://localhost:2136', database='/local')

# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)

def get_db():
    global db
    db = TinyDB('tmp/chat_db.json')
    return db


def register_chat(chat, register_req):
    def callee(session):
        # Create a transaction to perform a set of operations.
        transaction = session.transaction().begin()
        # Create a table object to perform operations on the table.
        table = transaction.table('chat')

        # Insert a new row into the table.
        table.insert(
            ('chat_id', chat.tg_chat_id),
            ('groupName', chat.group_name),
            ('disciplineName', chat.discipline_name),
            ('teacherName', chat.teacher_name),
            ('type', type(chat).__name__),
        )

        # Commit the transaction.
        transaction.commit()

    pool.retry_operation_sync(callee)

register_chat(GroupChat(1, 'ИУ5-31Б'), None)

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

