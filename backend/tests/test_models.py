import pytest
from django.test import TestCase
from pytest import fixture, mark

from users.models import MyUser
from food_shop.models import (
    Category,
    Subcategory,
    Product,
    ProductCart,
    ShoppingCartProduct
)


@pytest.fixture
def category():
    """
    Фикстура для создания тестовой категории с названием "Test_Category_Fruits".
    Возвращает:Category: Созданный объект Category.
    Дальше используем ее ниже как предзаготовку параметра category.
    """
    return Category.objects.create(
        name="Test_Category_Fruits",
        slug="test_category_fruits",
        icon=None
    )


@mark.django_db
class TestCategoryModel:
    """Тесты для модели Category."""

    def test_str_representation(self, category):
        """
        Проверка строкового представления модели Category.
        """
        assert str(category) == "Test_Category_Fruits"

    def test_slug_field(self, category):
        """
        Проверка, что поле slug не должно быть пустым и
        должно быть равно "test_category_fruits
        ."""
        assert category.slug is not None
        assert category.slug == "test_category_fruits"

    def test_icon_field(self, category):
        """
        Проверка что фото категории может быть пусто(None)
        """
        assert bool(category.icon) is False


