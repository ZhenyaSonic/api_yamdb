USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


USER_ROLES = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)


MAX_LENGTH_NAME = 150
"""Максимальная длина поля имени пользователя."""

MAX_LENGTH_EMAIL = 254
"""Максимальная длина поля email пользователя."""

MAX_LENGTH_BIO = 2000
"""Максимальная длина поля биографии пользователя."""

MAX_LENGTH_ROLE = max(len(role) for role, _ in USER_ROLES)
"""Максимальная длина поля роли пользователя."""
