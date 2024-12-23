-- name: ListUsers :many
SELECT
	users.*,
	CAST((MAX(telegram_users.id) IS NOT NULL) AS BOOLEAN) as telegram_activated,
	CAST(
		COALESCE(array_agg(user_blocks.blocked_id) FILTER (WHERE user_blocks.id IS NOT NULL), '{}')
		AS INTEGER[]
	) as users_blocked
FROM users
LEFT JOIN telegram_users ON users.telegram_id = telegram_users.id
LEFT JOIN user_blocks ON users.id = user_blocks.blocker_id
GROUP BY users.id
ORDER BY users.name;

-- name: CreateUser :one
WITH returned AS (
	INSERT INTO users (
	    name, telegram_id
	) VALUES (
	    $1, $2
	)
	RETURNING *
)
SELECT
	returned.*,
	CAST((telegram_users.id IS NOT NULL) AS BOOLEAN) as telegram_activated
FROM returned
LEFT JOIN telegram_users ON returned.telegram_id = telegram_users.id;

-- name: CheckUserExists :one
SELECT 1 FROM users WHERE id = $1 LIMIT 1;

-- name: UpdateUser :one
UPDATE users
SET
    name = COALESCE($2, name),
    telegram_id = COALESCE($3, telegram_id)
WHERE id = $1
RETURNING *;

-- name: GetUserByTelegramID :one
SELECT * FROM users
WHERE telegram_id = $1;

-- name: DeleteUser :exec
DELETE FROM users
WHERE id = $1;

-- name: ListUserBlocks :many
SELECT id, blocked_id FROM user_blocks
WHERE blocker_id = $1;

-- name: BlockUser :one
INSERT INTO user_blocks (
    blocker_id, blocked_id
) VALUES (
    $1, $2
)
RETURNING *;

-- name: UnblockUser :exec
DELETE FROM user_blocks
WHERE blocker_id = $1 and blocked_id = $2;

-- name: AddTelegramUser :exec
INSERT INTO telegram_users (id)
VALUES ($1)
ON CONFLICT DO NOTHING;

-- name: GetAdmin :one
SELECT * FROM admins
WHERE username = $1;

-- name: CreateAdmin :one
INSERT INTO admins (
    username, hashed_password
) VALUES (
    $1, $2
)
RETURNING *;