from enum import IntEnum


class LenghtField(IntEnum):
    """Длины полей в приложении Юзеров, Food_Shop."""

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

    # Атрибуты приложения Food_Shop
    # Максимальная длиная атрибутая name
    MAX_LENGT_NAME = 150
    # Максимальная длина слага тега slug
    MAX_LEN_SLUG = 150
    # Максимальная длина единицы измерения measurement_unit
    MAX_LENGT_MEASUREMENT_UNIT = 50
    # Количество продуктов в ShoppingCartProduct.amount
    MIN_AMOUNT_PRODUCT = 1
    MAX_AMOUNT_PRODUCT = 1000
    # Стоимость продукта в Product.price
    MIN_PRICE_PRODUCT = 1.0
    MAX_PRICE_PRODUCT = 10000.0
