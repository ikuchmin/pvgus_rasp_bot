## Overview

Here is Telegram Bot for pretty accessing PVGUS Student Scheduling (Telegram Bot для доступа к расписанию группы ;-)

Bot is running in Yandex Cloud and redy to run as stateless function 


## Register bot for a student group chat

Restrictions:
- only users with admin rights can register/unregister bot

1. Add bot to group chat
2. Send `/register_group <groupName>` command to bot

TODO

* ~~Сделать по умолчанию отображение только занятий которые идут сейчас и будущих~~
* ~~Сделать суффикс к командам _all чтобы видеть и прошлые занятия~~
* Add handling of case when user is not register chat for the group (now it just crashes)
* ~~Реализовать возможность регистрации чатов с помощью бота и ключа~~
* Реализовать возможность регистрации ссылок на SDO
* Подумать над deadline
* Добавить возможность посмотреть расписание на след неделю
* Нотификация с утра предупреждающая о занятиях сегодня
* Нотификация предупреждающая о начале занятий за 15 минут (required storage or just run before each pair of classes?)


## Create table

CREATE TABLE `chat`
(
`id` INT32 NOT NULL,
`disciplineName` String,
`groupName` String,
`teacherName` String,
`type` String,
`registerReq` Json,

    PRIMARY KEY (`id`)
);