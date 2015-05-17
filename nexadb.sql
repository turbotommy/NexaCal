CREATE TABLE test
(tsfrom DATETIME, tsto DATETIME, name TEXT);
CREATE TABLE suntimes(up DATETIME, down DATETIME);
CREATE UNIQUE INDEX pki_suntimes on suntimes (up asc,down asc);
CREATE TABLE booltest(test BOOLEAN);
CREATE TABLE NexaControl (eventId TEXT not null, name TEXT, updated DATETIME not null, tsfrom DATETIME not null, tsto DATETIME  not null, plugin TEXT, descr TEXT);
CREATE UNIQUE INDEX pki_NexaControl on NexaControl (eventId asc);
create table CalConfig (key TEXT, value TEXT);
CREATE TABLE NexaPlugins (eventId TEXT not null, name TEXT, updated DATETIME not null, eventType TEXT, eventRule TEXT);