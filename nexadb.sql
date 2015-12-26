CREATE TABLE suntimes(up DATETIME, down DATETIME);
CREATE UNIQUE INDEX pki_suntimes on suntimes (up asc,down asc);
--CREATE TABLE booltest(test BOOLEAN);
CREATE TABLE CalConfig (key TEXT, value TEXT);
CREATE TABLE NexaPlugins (eventId TEXT not null, name TEXT, updated DATETIME not null, eventType TEXT, eventRule TEXT, triggered INTEGER);
CREATE TABLE NexaControl (eventId TEXT not null, name TEXT, updated DATETIME not null, tsfrom DATETIME not null, tsto DATETIME  not null, plugin TEXT,status INTEGER);
CREATE UNIQUE INDEX pki_NexaControl on NexaControl (eventId asc);
CREATE INDEX i_NexaControl_2 on NexaControl (status, tsfrom asc);
CREATE TABLE NexaPlugins (eventId TEXT not null, name TEXT, updated DATETIME not null, eventType TEXT, eventRule TEXT);

select * from NexaControl where tsfrom <= (SELECT datetime('now','localtime')) and (status is null or status in(1, 979, 980)) order by tsfrom;

delete from NexaPlugins where eventid in (select eventid from NexaControl where tsfrom < '2015-07-20');
delete from NexaControl where tsfrom < '2015-07-20'