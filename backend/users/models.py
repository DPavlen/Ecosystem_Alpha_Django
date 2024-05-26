from core.constants import LenghtField
from core.validators import username_validator, validate_mobile, name_validator
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """
    Модель пользователя с дополнительными полями.
    Атрибуты:
        - USER: Константа для обозначения роли обычного пользователя.
        - ADMIN: Константа для обозначения роли администратора.
        - email: Поле для электронной почты пользователя.
        - username: Поле для логина пользователя.
        - first_name: Поле для Имя пользователя.
        - last_name: Поле для Фамилия пользователя.
        - phone: Поле для телефонного номера пользователя.
        - birth_date: Поле для даты рождения пользователя.
        - role: Поле для определения роли пользователя.
    """

    class RoleChoises(models.TextChoices):
        """
        Определение роли юзера.
        """

        USER = "user"
        ADMIN = "admin"

    email = models.EmailField(
        max_length=LenghtField.MAX_LENGHT_EMAIL.value,
        unique=True,
        verbose_name="email address",
    )
    username = models.CharField(
        "Логин пользователя",
        max_length=LenghtField.MAX_LENGHT_USERNAME.value,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        "Имя пользователя",
        max_length=LenghtField.MAX_LENGHT_FIRST_NAME.value,
        validators=[name_validator],
    )
    last_name = models.CharField(
        "Фамилия пользователя",
        max_length=LenghtField.MAX_LENGHT_LAST_NAME.value,
        validators=[name_validator],
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Телефон",
        unique=True,
        validators=[validate_mobile],
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="День Рождения пользователя"
    )
    role = models.TextField(
        "Пользовательская роль юзера",
        choices=RoleChoises.choices,
        default=RoleChoises.USER,
        max_length=LenghtField.MAX_LENGHT_ROLE.value,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id"]

    def __str__(self):
        return str(self.username)