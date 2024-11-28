CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    telegram_id INTEGER NOT NULL UNIQUE,
    flags INTEGER DEFAULT 0
);

CREATE TABLE user_blocks (
    id SERIAL PRIMARY KEY,
    blocker_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    blocked_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (blocker_id, blocked_id)
);

CREATE TABLE telegram_users (
    id BIGINT NOT NULL UNIQUE
);

CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
	hashed_password CHAR(60) NOT NULL
);

CREATE INDEX idx_user_blocks_blocker_id ON user_blocks(blocker_id);
CREATE INDEX idx_telegram_users_id ON telegram_users(id);