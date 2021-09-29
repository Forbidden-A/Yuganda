CREATE SCHEMA IF NOT EXISTS yuganda;


CREATE TABLE IF NOT EXISTS yuganda.guild_options (
    guild_id     BIGINT UNIQUE NOT NULL,
    starboard_id BIGINT DEFAULT NULL,
    PRIMARY KEY(guild_id)
);


CREATE TABLE IF NOT EXISTS yuganda.starred_messages (
    message_id   BIGINT UNIQUE NOT NULL,
    followup_id  BIGINT UNIQUE NOT NULL,
    stars        INT           NOT NULL,
    PRIMARY KEY(message_id)
);
