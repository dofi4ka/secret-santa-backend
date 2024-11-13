-- name: ListUsers :many
SELECT users.*, (telegram_users.id IS NOT NULL) as telegram_activated FROM users
LEFT JOIN telegram_users ON users.telegram_id = telegram_users.id;

-- name: CreateUser :one
INSERT INTO users (
    name, telegram_id
) VALUES (
    $1, $2
)
RETURNING *;

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
VALUES ($1);

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