CREATE SCHEMA IF NOT EXISTS yuganda;

CREATE TABLE IF NOT EXISTS yuganda.starboard (
    post_id BIGINT NOT NULL,
    followup_id BIGINT NOT NULL,
    stars INT NOT NULL
    PRIMARY KEY(post_id)
)