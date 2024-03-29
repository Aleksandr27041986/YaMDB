import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        ('user', USER),
        ('moderator', MODERATOR),
        ('admin', ADMIN)
    ]
    email = models.EmailField('Email', unique=True, max_length=254)
    username = models.CharField(
        'Никнеим',
        max_length=150,
        unique=True,
        help_text=('Обязательное поле, только цифры, буквы или @/./+/-/_.'),
        validators=[UnicodeUsernameValidator()],
        blank=True,
        null=True,
    )
    bio = models.TextField(
        'О себе',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Статус',
        max_length=16,
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True,
        default=uuid.uuid4
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff
