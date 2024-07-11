import pytest
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    DateTimeField,
    DecimalField,
    ImageField,
    ForeignKey,
    PositiveSmallIntegerField
)
from django.test import TestCase
from gunicorn.config import User
from pytest import mark
from pytest_django.asserts import assertRaisesMessage

from core.constants import LenghtField
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


@mark.django_db
class TestSubcategoryModel(TestCase):
    """Тесты для модели подкатегории(Subcategory)."""

    def test_str_representation(self):
        """
        Проверка строкового представления модели Subcategory.
        """
        category = Category.objects.create(name="Test_Category_Fruits")
        subcategory = Subcategory.objects.create(
            name="Test_Subcategory_Berries",
            category=category,
        )
        assert str(subcategory) == "Test_Subcategory_Berries"

    def test_models_fields(self):
        """
        Проверка полей модели подкатегории(Subcategory).
        """
        fields = Subcategory._meta.fields
        fields_names = [field.name for field in fields]
        assert "name" in fields_names
        assert "category" in fields_names
        assert "slug" in fields_names
        assert "icon" in fields_names

    def test_fields_types(self):
        """
        Проверка типов полей модели подкатегории(Subcategory).
        """
        assert isinstance(Subcategory._meta.get_field("name"), CharField)
        assert isinstance(Subcategory._meta.get_field("category"), ForeignKey)
        assert isinstance(Subcategory._meta.get_field("slug"), AutoSlugField)
        assert isinstance(Subcategory._meta.get_field("icon"), ImageField)


@mark.django_db
class TestProductModel(TestCase):
    """Тесты для модели продукта(Product)."""

    def test_models_fields(self):
        """
        Проверка полей модели продукта(Product).
        """
        fields = Product._meta.fields
        fields_name = [field.name for field in fields]
        assert "name" in fields_name
        assert "subcategory" in fields_name
        assert "slug" in fields_name
        assert "price" in fields_name
        assert "measurement_unit" in fields_name
        assert "icon_small" in fields_name
        assert "icon_middle" in fields_name
        assert "icon_big" in fields_name
        assert "date_add" in fields_name

    def test_fields_types(self):
        """
        Проверка типов полей модели продукта(Product).
        """
        assert isinstance(Product._meta.get_field("name"), CharField)
        assert isinstance(Product._meta.get_field("subcategory"), ForeignKey)
        assert isinstance(Product._meta.get_field("slug"), AutoSlugField)
        assert isinstance(Product._meta.get_field("price"), DecimalField)
        assert isinstance(Product._meta.get_field("measurement_unit"), CharField)
        assert isinstance(Product._meta.get_field("icon_small"), ImageField)
        assert isinstance(Product._meta.get_field("icon_middle"), ImageField)
        assert isinstance(Product._meta.get_field("icon_big"), ImageField)
        assert isinstance(Product._meta.get_field("date_add"), DateTimeField)

    def test_price_min_validation(self):
        """
        Проверка валидации поля "Стоимость продукта"-min price.
        """
        category = Category.objects.create(name="Test_Category_Fruits")
        subcategory = Subcategory.objects.create(
            name="Test_Subcategory_Berries",
            category=category
        )

        product = Product(
            name="Test_Product_Чернослив",
            subcategory=subcategory,
            price=0
        )
        with self.assertRaisesMessage(
                ValidationError,
                "['Минимальное стоимость продукта должна быть не меньше 1.']"
        ):
            product.full_clean()

    def test_price_max_validation(self):
        """
        Проверка валидации поля "Стоимость продукта"-max price.
        """
        category = Category.objects.create(name="Test_Category_Fruits")
        subcategory = Subcategory.objects.create(
            name="Test_Subcategory_Berries",
            category=category
        )

        product = Product(
            name="Test_Product_Чернослив",
            subcategory=subcategory,
            price=10009
        )

        with self.assertRaisesMessage(
                ValidationError,
                "['Максимальная стоимость продукта должна быть не больше 10000.']"
        ):
            product.full_clean()


@pytest.mark.django_db
class TestProductCartModel(TestCase):
    """Тесты для продуктовой корзины(ProductCart) у покупателя-пользователя."""

    def test_models_fields(self):
        """
        Проверка полей модели ProductCart(ProductCart).
        """
        fields = ProductCart._meta.fields
        fields_names = [field.name for field in fields]
        assert "user" in fields_names
        assert "date_created" in fields_names

    def test_fields_types(self):
        """
        Проверка типов полей модели продукта(Product).
        """
        assert isinstance(ProductCart._meta.get_field("user"), ForeignKey)
        assert isinstance(ProductCart._meta.get_field("date_created"), DateTimeField)

    def test_str_representation(self):
        """
         Проверка строкового представления модели продуктовой корзины(ProductCart).
        """
        user = MyUser.objects.create(
            username="Test_user"
        )
        product_cart = ProductCart.objects.create(
            user=user
        )
        assert (
                str(product_cart) == f"Покупатель-пользователь {product_cart.user}"
        )


@pytest.mark.django_db
class TestShoppingCartProductModel(TestCase):
    """Тесты для корзины покупок товаров(ShoppingCartProduct)
     у покупателя-пользователя."""

    def test_models_fields(self):
        """
        Проверка полей модели корзины покупок товаров (ShoppingCartProduct)
        у покупателя-пользователя
        .
        """
        fields = ShoppingCartProduct._meta.fields
        fields_names = [field.name for field in fields]
        assert "product_cart" in fields_names
        assert "product" in fields_names
        assert "amount" in fields_names
        assert "date_created" in fields_names

    def test_fields_types(self):
        """
        Проверка типов полей модели корзины
        покупок товаров (ShoppingCartProduct).
        """
        assert isinstance(
            ShoppingCartProduct._meta.get_field("product_cart"), ForeignKey)
        assert isinstance(
            ShoppingCartProduct._meta.get_field("product"), ForeignKey)
        assert isinstance(
            ShoppingCartProduct._meta.get_field("amount"), PositiveSmallIntegerField)
        assert isinstance(
            ShoppingCartProduct._meta.get_field("date_created"), DateTimeField)

    def test_str_representation(self):
        """
        Проверка строкового представления модели корзины
        покупок товаров (ShoppingCartProduct) у покупателя-пользователя..
        """
        user = MyUser.objects.create(
            username="Test_user"
        )
        product_cart = ProductCart.objects.create(
            user=user
        )
        category = Category.objects.create(
            name="Test_Category_Фрукты"
        )
        subcategory = Subcategory.objects.create(
            name="Test_Subcategory_Цитрусовые",
            category=category
        )
        product = Product.objects.create(
            name="Test_product_Lemon",
            price="50",
            subcategory=subcategory,
            measurement_unit="шт"
        )
        shopping_cart_product = ShoppingCartProduct.objects.create(
            product_cart=product_cart,
            product=product,
            amount=12
        )
        expected_str = (f"В продуктовой козине - пользователя {product_cart.user},"
                        f" {product.name} в количестве {shopping_cart_product.amount} "
                        f" {product.measurement_unit}")
        assert str(shopping_cart_product) == expected_str
