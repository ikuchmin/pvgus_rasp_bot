CREATE TABLE `/local/chat`
(
    `tgChatId`        Utf8,
    `type`            Utf8,
    `disciplineName`  Utf8,
    `groupName`       Utf8,
    `teacherName`     Utf8,
    `registerRequest` Json,
    PRIMARY KEY (`tgChatId`)
);