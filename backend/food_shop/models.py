from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from autoslug import AutoSlugField
from PIL import Image
from transliterate import translit

from core.constants import LenghtField
from users.models import MyUser


def get_slug(instance):
    """
    Транслитерованный слаг для
    категорий, подкатегорий и продуктов.
    """

    return translit(
        instance.name,
        'ru',
        reversed=True)


def resize_image(image, max_size):
    """
     Изменяет размер изображения, сохраняя его пропорции, так чтобы
    ни ширина, ни высота не превышали заданное максимальное значение.
    Параметры:
    image (File): Файл изображения, который нужно изменить.
    max_size (int): Максимальное значение для ширины и высоты изображения.
    Возвращает:
    None: Функция изменяет размер изображения на месте и сохраняет его
          в том же файле.
    """

    img = Image.open(image)
    img.thumbnail((max_size, max_size))
    img.save(image.path)


class Category(models.Model):
    """
    Модель категорий товаров.
    Атрибуты:
        - name: Название категории.
        - slug: Уникальный слаг категории.
        - icon: Фото категории.
    """
    name = models.CharField(
        max_length=LenghtField.MAX_LENGT_NAME.value,
        verbose_name="Название категории"
    )
    slug = AutoSlugField(
        max_length=LenghtField.MAX_LEN_SLUG.value,
        populate_from=get_slug,
        unique=True,
        verbose_name="Слаг категории"
    )
    icon = models.ImageField(
        verbose_name="Фото категории",
        upload_to="categories",
        default=None,
        blank=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """
        Возвращает строковое представление категории.
        Returns: str: Название категории.
        """
        return self.name


class Subcategory(models.Model):
    """
    Модель подкатегории товара.
    Атрибуты:
        - name: Название подкатегории.
        - category: Связанная категория.
        - slug: Уникальный слаг подкатегории.
        - icon: Фото подкатегории.
    """

    name = models.CharField(
        unique=True,
        max_length=LenghtField.MAX_LENGT_NAME.value,
        verbose_name="Название",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория"
    )
    slug = AutoSlugField(
        unique=True,
        max_length=LenghtField.MAX_LEN_SLUG.value,
        populate_from=get_slug,
        verbose_name="Cлаг подкатегории"
    )
    icon = models.ImageField(
        "Фото подкатегории",
        upload_to="subcategories",
        default=None,
        blank=True,
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ("name",)

    def __str__(self):
        """
        Возвращает строковое представление подкатегории.
        Returns: str: Название категории.
        """

        return self.name


class Product(models.Model):
    """
    Модель продукта.
    Атрибуты:
        - name: Название продукта.
        - subcategory: Подкатегория продукта.
        - slug: Уникальный слаг продукта.
        - price: Стоимость продукта.
        - measurement_unit: Единица измерения.
        - icon_small: Маленькое фото продукта.
        - icon_middle: Среднее фото продукта.
        - icon_big: Большое фото продукта.
        - date_add: Дата добавления продукта.
    """

    UNIT_CHOICES = (
        ("kg", "Килограммы"),
        ("lt", "Литры"),
        ("pcs", "Штуки"),
    )
    name = models.CharField(
        unique=True,
        max_length=LenghtField.MAX_LENGT_NAME.value,
        verbose_name="Название продукта"
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Подкатегория"
    )
    slug = AutoSlugField(
        unique=True,
        max_length=LenghtField.MAX_LEN_SLUG.value,
        populate_from=get_slug,
        verbose_name="Cлаг продукта"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость продукта",
        validators=[
            MinValueValidator(
                LenghtField.MIN_PRICE_PRODUCT.value,
                message=f"Минимальное стоимость продукта "
                        f"должна быть не меньше "
                        f"{LenghtField.MIN_PRICE_PRODUCT.value}.",
            ),
            MaxValueValidator(
                LenghtField.MAX_PRICE_PRODUCT.value,
                message=f"Максимальная стоимость продукта "
                        f"должна быть не больше "
                        f"{LenghtField.MAX_PRICE_PRODUCT.value}.",
            ),
        ],
    )
    measurement_unit = models.CharField(
        max_length=LenghtField.MAX_LENGT_MEASUREMENT_UNIT.value,
        choices=UNIT_CHOICES,
        default="kg",
        verbose_name="Единица измерения"
    )
    icon_small = models.ImageField(
        upload_to="products_small/",
        blank=True,
        null=True,
        verbose_name="Фото продукта маленькое",
    )
    icon_middle = models.ImageField(
        upload_to="products_middle/",
        blank=True,
        null=True,
        verbose_name="Фото продукта среднее",
    )
    icon_big = models.ImageField(
        upload_to="products_big/",
        blank=True,
        null=True,
        verbose_name="Фото продукта большое",
    )
    date_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления продукта"
    )

    def save(self, *args, **kwargs):
        """
        Сохраняет текущий экземпляр и изменяет размер связанных изображений.
        Есть ли у экземпляра изображения, назначенные полям `icon_small`,
        `icon_middle` и `icon_big`, и изменяет их размер до предопределенных
        размеров с помощью утилиты `resize_image`.
        Параметры:
        *args: Список аргументов переменной длины.
        **kwargs: Произвольные именованные аргументы.
        Возвращает: None
            """
        super().save(*args, **kwargs)
        if self.icon_small:
            resize_image(self.icon_small, 200)
        if self.icon_middle:
            resize_image(self.icon_middle, 400)
        if self.icon_big:
            resize_image(self.icon_big, 600)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-date_add"]

    def __str__(self):
        """
        Возвращает строковое представление продукта.
        Returns: str: Название продукта.
        """

        return self.name


class ProductCart(models.Model):
    """
    Модель продуктовой корзины у покупателя-пользователя.
    Атрибуты:
        - user: Пользователь, владеющий корзиной.
        - date_created: Дата создания корзины.
    """

    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь продуктовой корзины"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания продуктовой корзины"
    )

    class Meta:
        verbose_name = "Продуктовая корзина"
        verbose_name_plural = "Продуктовые корзины"
        ordering = ["-date_created"]

    def __str__(self):
        """
        Возвращает строковое представление пользователя корзины.
        Returns: str: имя пользователя.
        """
        return f"Покупатель-пользователь {self.user}"


class ShoppingCartProduct(models.Model):
    """
    Модель корзины покупок товаров.
    Связка между продуктовой корзиной покупателя-пользователя и продуктами.
    Атрибуты:
        - product_cart: Продуктовая корзина пользователя.
        - product: Продукт в корзине.
        - amount: Количество продуктов в корзине.
        - date_created: Дата создания корзины покупок пользователя.
    """

    product_cart = models.ForeignKey(
        ProductCart,
        on_delete=models.CASCADE,
        related_name="shopping_cart_products",
        verbose_name="Продуктовая корзина",
        db_index=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="shopping_cart_products",
        verbose_name="Продукт",
        db_index=True,
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество продуктов в корзине",
        validators=[
            MinValueValidator(
                LenghtField.MIN_AMOUNT_PRODUCT.value,
                message=f"Минимальное количество продукта "
                        f"должно быть не меньше "
                        f"{LenghtField.MIN_AMOUNT_PRODUCT.value}.",
            ),
            MaxValueValidator(
                LenghtField.MAX_AMOUNT_PRODUCT.value,
                message=f"Максимально количество продукта "
                        f"не превышает {LenghtField.MAX_AMOUNT_PRODUCT.value}.",
            ),
        ],
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания корзины покупок пользователя"
    )

    class Meta:
        verbose_name = "Продукт в корзине у пользователя"
        verbose_name_plural = "Продукты в корзинах у пользователей"
        ordering = ["-date_created"]

    def __str__(self):
        """
        Возвращает строковое представление продукта в корзине.
        Returns:
        str: Описание продукта в корзине с количеством и единицей измерения.
        """

        return (f"В продуктовой козине - пользователя {self.product_cart.user},"
                f" {self.product.name} в количестве {self.amount} "
                f" {self.product.measurement_unit}")




