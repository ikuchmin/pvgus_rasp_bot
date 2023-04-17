from tinydb import TinyDB, Query

from tg_bot.marshal import serialize, deserialize
from common.types import GroupChat, StudentGroupChat, StudentGroupDisciplineChat, TeacherChat
from common.types import Chat
import dataclasses
from dataclasses import dataclass, asdict
import json
import os
import ydb
import ydb.iam

global db


database=os.getenv('YDB_DATABASE')
endpoint=os.getenv('YDB_ENDPOINT')

# Create driver in global space.
driver = ydb.Driver(endpoint=endpoint, database=database,
                    credentials=ydb.iam.MetadataUrlCredentials())
# os.environ['GRPC_DNS_RESOLVER'] = 'native'
# driver = ydb.Driver(endpoint='grpc://localhost:2136', database='/local')

# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)


def get_db():
    global db
    db = TinyDB('tmp/chat_db.json')
    return db


def find_chat(chat_id):
    def callee(session):
        # Create a transaction to perform a set of operations.
        query = f"""
            PRAGMA TablePathPrefix("{database}");
            DECLARE $id AS INT32;
            
            SELECT * FROM chat WHERE id = $id;
        """

        prepared_query = session.prepare(query)

        return session.transaction().execute(prepared_query, parameters={
            "$id": chat_id,
        }, commit_tx=True)

    rs = pool.retry_operation_sync(callee)

    return __chat_from_rs(rs[0].rows[0])


def find_all_chat():
    def callee(session):
        # Create a transaction to perform a set of operations.
        query = f"""
            PRAGMA TablePathPrefix("{database}");
            
            SELECT * FROM chat;
        """

        prepared_query = session.prepare(query)

        return session.transaction().execute(prepared_query, commit_tx=True)

    return pool.retry_operation_sync(callee)


def register_group_chat(chat: StudentGroupChat, register_req):
    c = Chat(**dataclasses.asdict(chat))
    register_chat(c, register_req)


def register_group_discipline_chat(chat: StudentGroupDisciplineChat, register_req):
    c = Chat(**dataclasses.asdict(chat))
    register_chat(c, register_req)


def register_teacher_chat(chat: TeacherChat, register_req):
    c = Chat(**dataclasses.asdict(chat))
    register_chat(c, register_req)


def register_chat(chat, register_req):
    def callee(session):
        # Create a transaction to perform a set of operations.
        query = f"""
            PRAGMA TablePathPrefix("{database}");
            DECLARE $id AS INT32;
            DECLARE $groupName AS Utf8?;
            DECLARE $disciplineName AS Utf8?;
            DECLARE $teacherName AS Utf8?;
            DECLARE $type AS Utf8;
            DECLARE $registerReq AS Json;

            INSERT INTO chat (id, groupName, disciplineName, teacherName, type, registerReq)
            VALUES ($id, $groupName, $disciplineName, $teacherName, $type, $registerReq)
        """

        prepared_query = session.prepare(query)

        session.transaction().execute(prepared_query, parameters={
            "$id": chat.tgChatId,
            "$groupName": chat.groupName,
            "$disciplineName": chat.disciplineName,
            "$teacherName": chat.teacherName,
            "$type": chat.type.name,
            "$registerReq": json.dumps(register_req),
        }, commit_tx=True)

    pool.retry_operation_sync(callee)


def delete_chat(chat_id):
    def callee(session):
        # Create a transaction to perform a set of operations.
        query = f"""
            PRAGMA TablePathPrefix("{database}");
            DECLARE $id AS INT32;

            DELETE FROM chat WHERE id == $id;
        """

        prepared_query = session.prepare(query)

        session.transaction().execute(prepared_query, parameters={
            "$id": chat_id,
        }, commit_tx=True)

    pool.retry_operation_sync(callee)


def create_chat(tg_chat):
    db = get_db()
    Chat = Query()

    db.upsert(serialize(tg_chat), Chat.chat_id == tg_chat.tg_chat_id)


# def find_chat(chat_id):
#     db = get_db()
#     Chat = Query()
#
#     chats_raw = db.search(Chat.chat_id == chat_id)
#     if len(chats_raw) == 0:
#         return None
#
#     chat_raw = chats_raw[0]
#
#     return deserialize(chat_raw)

# def find_all_chats():
#     db = get_db()
#     chats_raw = db.all()
#
#     return [deserialize(chat_raw) for chat_raw in chats_raw]

def __chat_from_rs(rs):
    # remap id to tgChatId
    m = {('tgChatId' if k == 'id' else k): v for k, v in rs.items()}

    # decode bytes to string
    m = {k: v.decode() if isinstance(v, bytes) else v for k, v in m.items()}

    if rs.type == 'GroupChat'.encode():
        return StudentGroupChat.from_dict(m)