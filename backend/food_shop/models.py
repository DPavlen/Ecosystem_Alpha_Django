from django.db import models
from autoslug import AutoSlugField
# from mptt.models import MPTTModel, TreeForeignKey
from transliterate import translit

from users.models import MyUser


def get_slug(instance):
    """Транслитерованный слаг для
    категорий и подкатегорий товаров."""
    return translit(
        instance.name,
        'ru',
        reversed=True)


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
    name = models.CharField(
        unique=True,
        max_length=250,
        verbose_name="Название продукта"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
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

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("date_add",)

    def __str__(self):
        return f"{self.name}"


class ProductCart(models.Model):
    """Модель продуктовой корзины у покупателя-пользователя."""
    buyer = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь продуктовой корзины"
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания продуктовой корзины"
    )

    class Meta:
        verbose_name = "Продуктовая корзина"
        verbose_name_plural = "Продуктовые корзины"
        ordering = ("date_create",)

    def __str__(self):
        return f"Покупатель {self.buyer}"


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
        verbose_name="Количество"
    )

    class Meta:
        unique_together = ("product_cart", "product")
        verbose_name = "Продукт в корзине у пользователя"
        verbose_name_plural = "Продукты в корзинах у пользователей"

    def __str__(self):
        return f"В продуктовой козине {self.product.name} - {self.amount} шт."




