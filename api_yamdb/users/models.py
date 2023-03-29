from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = [
    ('user', USER),
    ('moderator', MODERATOR),
    ('admin', ADMIN)
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.TextField(
        'Роль',
        blank=True,
        choices=ROLES,
        default=USER
    )