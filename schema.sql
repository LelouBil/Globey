create table global_mutes
(
	user_id int not null
		primary key
)
;

create unique index global_mutes_user_id_uindex
	on global_mutes (user_id)
;

create table servers
(
	server_id int not null
		primary key,
	server_name text not null
)
;

create table global_channels
(
	channel_id integer not null
		primary key,
	server_id integer not null
		references servers,
	channel_name TEXT not null,
	webhook_id integer default 0 not null,
	webhook_token TEXT default 0 not null
)
;

create table server_preferences
(
	pref_key TEXT not null,
	pref_value TEXT not null,
	server_id integer not null
		references servers,
	primary key (pref_key, server_id)
)
;

