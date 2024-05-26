from enum import IntEnum


class LenghtField(IntEnum):
    """Длины полей в приложении Юзеров и т.д."""

    # Атрибуты приложения Юзеров
    # Максимальная длина поля email User.email
    MAX_LENGHT_EMAIL = 254
    # Максимальная длина поля username User.username
    MAX_LENGHT_USERNAME = 150
    # Максимальная длина поля first_name User.first_name
    MAX_LENGHT_FIRST_NAME = 150
    # Максимальная длина поля last_name User.last_name
    MAX_LENGHT_LAST_NAME = 150
    # Максимальная длина поля password User.password
    MAX_LENGHT_PASSWORD = 150
    # Максимальная длина поля role User.role
    MAX_LENGHT_ROLE = 150

    # page_size = 10 for API PaginationCust.page_size
    PAGE_SIZE = 10

    # Минимальная длина логина пользователя
    MIN_LENGHT_LOGIN_USER = 1
    # Минимальная длина поля first_name
    MIN_LENGHT_FIRST_NAME = 1
    # Минимальная длина поля last_name
    MIN_LENGHT_LAST_NAME = 1