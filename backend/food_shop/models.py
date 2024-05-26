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
    description = models.CharField(
        max_length=250,
        default=None,
        blank=True,
        verbose_name="Описание категории"
    )
    icon = models.ImageField(
        verbose_name="Фото категории",
        upload_to="food_shop/images/categories",
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
        "Изображение",
        upload_to="food_shop/images/subcategories",
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