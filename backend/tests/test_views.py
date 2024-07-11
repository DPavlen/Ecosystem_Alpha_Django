from gunicorn.config import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


from food_shop.models import (
    Category, Subcategory, Product, ProductCart, ShoppingCartProduct)
from users.models import MyUser


class TestProductViewSet(APITestCase):
    """
    Тесты для проверки функциональности корзины покупок пользователя.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Установка начальных данных для всех тестов в классе.
        Этот метод вызывается один раз для установки данных, которые будут
        использоваться всеми тестовыми методами в данном классе.
        """
        cls.user_one = MyUser.objects.create_user(
            username="Usertest_1",
            email="usertest1@example.com",
            password="Passwordpass1"
        )
        cls.user_two = MyUser.objects.create_user(
            username="Usertest_2",
            email="usertest2@example.com",
            password="Passwordpass2"
        )
        cls.category = Category.objects.create(
            name="Test_Category_Fruits",
            slug="test_category_fruits",
            icon=None
        )
        cls.subcategory = Subcategory.objects.create(
            name="Test_Subcategory_Berries",
            category=cls.category,
        )
        cls.product = Product.objects.create(
            name="Test_Product_Чернослив",
            subcategory=cls.subcategory,
            slug="Test_Product_chernosliv",
            price=100,
            measurement_unit="kg",
            icon_small=None,
            icon_middle=None,
            icon_big=None
        )

    def setUp(self):
        """
        Создаёт экземпляр APIClient, который будет использоваться для выполнения
        HTTP-запросов в тестах.
        """
        self.client = APIClient()

    def get_authenticated_client(self, user):
        """
        Возвращает аутентифицированный клиент для пользователя.
        """
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + str(token.key)
        )
        return self.client

    def test_product_list(self):
        """
        Тест для получения списка продуктов.
        GET-запрос "product-list" и ответ - 200 OK.
        """
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], self.product.name)

    def test_product_detail(self):
        """
        Тест для получения деталей конкретного продукта.
        GET-запрос "product-detail" с ID продукта и ответ - 200 OK.
        """

        url = reverse("product-detail", kwargs={"pk": self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ShoppingCartProductViewSet(APITestCase):
    """
    Тесты для проверки функциональности продуктовой корзины(ShoppingCartProduct).
    """
    @classmethod
    def setUpTestData(cls):
        """
        Установка начальных данных для всех тестов в классе.
        Этот метод вызывается один раз для установки данных, которые будут
        использоваться всеми тестовыми методами в данном классе.
        """
        cls.user_one = MyUser.objects.create_user(
            username="Usertest_1",
            email="usertest1@example.com",
            password="Passwordpass1"
        )
        cls.user_two = MyUser.objects.create_user(
            username="Usertest_2",
            email="usertest2@example.com",
            password="Passwordpass2"
        )
        cls.category = Category.objects.create(
            name="Test_Category_Fruits",
            slug="test_category_fruits",
            icon=None
        )
        cls.subcategory = Subcategory.objects.create(
            name="Test_Subcategory_Berries",
            category=cls.category,
        )
        cls.product = Product.objects.create(
            name="Test_Product_Чернослив",
            subcategory=cls.subcategory,
            slug="Test_Product_chernosliv",
            price=100,
            measurement_unit="kg",
            icon_small=None,
            icon_middle=None,
            icon_big=None
        )
        cls.product_cart = ProductCart.objects.create(
            user=cls.user_one
        )

    def setUp(self):
        """
        Создаёт экземпляр APIClient, который будет использоваться для выполнения
        HTTP-запросов в тестах.
        """
        self.client = APIClient()

    def get_authenticated_client(self, user):
        """
        Возвращает аутентифицированный клиент для пользователя.
        """
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + str(token.key)
        )
        return self.client

    def test_shoppingcartproduct_create_authenticated(self):
        """
        Тест создания продукта в продуктовую корзину
        аутентифициров§анным пользователем.
        """
        client = self.get_authenticated_client(self.user_one)
        url = reverse("shoppingcartproduct-list")
        data = {
            "product_cart": self.product_cart.id,
            "product": self.product.id,
            "amount": 10,
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверим продукт в созданной продуктовой корзине пользователя
        created_cart_product = ShoppingCartProduct.objects.get(
            product_cart=self.product_cart, product=self.product)
        self.assertEqual(created_cart_product.amount, 10)
        self.assertEqual(created_cart_product.product, self.product)
        self.assertEqual(created_cart_product.product_cart, self.product_cart)
        self.assertTrue(ShoppingCartProduct.objects.filter(
            product=self.product).exists())

    def test_shoppingcartproduct_create_unauthenticated(self):
        """
        Тест создания продукта в продуктовую корзину пользователя,
        неаутентифицированным пользователем.
        """

        url = reverse("shoppingcartproduct-list")
        data = {
            "product_cart": self.product_cart.id,
            "product": self.product.id,
            "amount": 10,
        }
        # Отправляем запрос без аутентификации пользователя!
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
