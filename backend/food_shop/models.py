from django.db import models
from autoslug import AutoSlugField
from PIL import Image
from transliterate import translit

from users.models import MyUser


def get_slug(instance):
    """Транслитерованный слаг для
    категорий и подкатегорий товаров."""
    return translit(
        instance.name,
        'ru',
        reversed=True)


def resize_image(image, max_size):
    """Функция для изменения размера изображения"""
    img = Image.open(image)
    img.thumbnail((max_size, max_size))
    img.save(image.path)


class Category(models.Model):
    """Модель категорий товаров."""
    name = models.CharField(
        max_length=20,
        verbose_name="Название категории"
    )
    slug = AutoSlugField(
        max_length=255,
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
        Dunder-метод для отображения имени категории как строки.
        """
        return self.name


class Subcategory(models.Model):
    """Модель подкатегории товара."""
    name = models.CharField(
        unique=True,
        max_length=250,
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
        max_length=200,
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
        verbose_name = "подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ("name",)

    def __str__(self):
        """
        Dunder-метод для отображения имени подкатегории как строки.
        """

        return self.name


class Product(models.Model):
    """Модель продукта."""
    UNIT_CHOICES = (
        ("kg", "Килограммы"),
        ("lt", "Литры"),
        ("pcs", "Штуки"),
    )
    name = models.CharField(
        unique=True,
        max_length=250,
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
        max_length=200,
        populate_from=get_slug,
        verbose_name="Cлаг продукта"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость продукта"
    )
    measurement_unit = models.CharField(
        max_length=50,
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
        return f"{self.name}"


class ProductCart(models.Model):
    """Модель продуктовой корзины у покупателя-пользователя."""
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
        return f"Покупатель {self.user}"


class ShoppingCartProduct(models.Model):
    """Модель корзины покупок товаров.
    Связка между продуктовой корзины покупателя-пользователя
    и продуктами.
    """
    product_cart = models.ForeignKey(
        ProductCart,
        on_delete=models.CASCADE,
        related_name="shopping_cart_products",
        verbose_name="Продуктовая корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Продукт"
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество продуктов в корзине"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания корзины покупок пользователя"
    )

    class Meta:
        unique_together = ("product_cart", "product")
        verbose_name = "Продукт в корзине у пользователя"
        verbose_name_plural = "Продукты в корзинах у пользователей"
        ordering = ["-date_created"]

    def __str__(self):
        return f"В продуктовой козине {self.product.name} - {self.amount} шт."




