CREATE TABLE suntimes(up DATETIME, down DATETIME);
CREATE UNIQUE INDEX pki_suntimes on suntimes (up asc,down asc);
--CREATE TABLE booltest(test BOOLEAN);
CREATE TABLE CalConfig (key TEXT, value TEXT);
CREATE TABLE NexaControl (eventId TEXT not null, name TEXT, updated DATETIME not null, tsfrom DATETIME not null, tsto DATETIME  not null, plugin TEXT,status INTEGER);
CREATE UNIQUE INDEX pki_NexaControl on NexaControl (status, eventId asc);
CREATE TABLE NexaPlugins (eventId TEXT not null, name TEXT, updated DATETIME not null, eventType TEXT, eventRule TEXT);
