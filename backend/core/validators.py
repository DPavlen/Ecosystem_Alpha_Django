import re
from re import search

from django.core.exceptions import ValidationError


def username_validator(username):
    """Валидация для поля 'Логин пользователя' модели User."""
    if username == "me":
        raise ValidationError("Нельзя использовать имя пользователя me")

    if not search(r"^[a-zA-Z][a-zA-Z0-9-_.]{1,150}$", username):
        raise ValidationError("В логине Пользователя используются недопустимые символы")


def name_validator(name):
    """Общий валидатор для полей 'Имя пользователя' и 'Фамилия пользователя' модели User."""
    if not search(r"^[A-Za-zА-Яа-я0-9]{1,150}$", name):
        raise ValidationError("В поле пользователя используются недопустимые символы")


def validate_mobile(value):
    """Валидация для поля "Телефон"."""
    rule = re.compile(r"^\+?[7-8]?[0-9]{10}$")

    if not rule.search(value):
        raise ValidationError("Неверный мобильный номер.")