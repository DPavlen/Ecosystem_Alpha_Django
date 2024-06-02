from django.db.models import F, Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions

from api.v1.permissions import IsOwnerOrReadOnlyOrAdmin
from api.v1.serializers import (
    CategorySerializer,
    SubcategorySerializer,
    ProductSerializer,
    ShoppingCartProductSerializer,
    ShoppingCartSummarySerializer,
)
from core.pagination import PaginationCust
from food_shop.models import (
    Category,
    Subcategory,
    Product,
    ShoppingCartProduct,
    ProductCart,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Кастомный ViewSet для работы с категориями.
    Attributes:
        - queryset: QuerySet для получения всех категорий.
        - serializer_class: Сериализатор для категорий.
        - permission_classes: Классы разрешений для доступа к категориям.
        - pagination_class: Пагинация для категорий.
    """

    queryset = Category.objects.prefetch_related("subcategories")
    serializer_class = CategorySerializer
    permission_classes = permissions.AllowAny()
    pagination_class = PaginationCust


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Кастомный ViewSet для работы с подкатегориями.
    Attributes:
        - queryset: QuerySet для получения всех подкатегорий с привязкой к категориям.
        - serializer_class: Сериализатор для подкатегорий.
        - permission_classes: Классы разрешений для доступа к подкатегориям.
        - pagination_class: Пагинация для подкатегорий.
    """

    queryset = Subcategory.objects.select_related("category")
    serializer_class = SubcategorySerializer
    permission_classes = permissions.AllowAny()
    pagination_class = PaginationCust


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Кастомный ViewSet для работы с продуктами.
    Атрибуты:
    - queryset: Запрос к модели Product с предварительной загрузкой
     связанных моделей: "subcategory" и "category"
    - serializer_class: Сериализатор для продуктов.
    - permission_classes: Классы разрешений для доступа к продуктам.
    - pagination_class: Пагинация для продуктов.
    """

    queryset = Product.objects.select_related("subcategory").prefetch_related(
        "subcategory__category"
    )
    serializer_class = ProductSerializer
    permission_classes = permissions.AllowAny()
    pagination_class = PaginationCust


class ShoppingCartProductViewSet(viewsets.ModelViewSet):
    """
    Кастомный ViewSet для работы с продуктовой корзиной.
    Атрибуты:
        queryset (QuerySet): Запрос к модели "ShoppingCartProduct"
        для получения всех элементов корзины.
        serializer_class (Serializer): Класс сериализатора для продуктовой корзины.
        permission_classes (tuple): Классы разрешений для доступа к продуктовой корзине.
        pagination_class (Paginator): Класс пагинации для продуктовой корзины.
    """

    queryset = ShoppingCartProduct.objects.all()
    serializer_class = ShoppingCartProductSerializer
    pagination_class = PaginationCust

    def get_permissions(self):
        """
        Возвращает соответствующие разрешения в зависимости от действия.
        :return: Кортеж с разрешениями, соответствующими действию.
        """

        action_permissions = {
            "list": (permissions.AllowAny(),),
            "retrieve": (permissions.AllowAny(),),
            "create": (permissions.IsAuthenticated(),),
            "update": (IsOwnerOrReadOnlyOrAdmin(),),
            "partial_update": (IsOwnerOrReadOnlyOrAdmin(),),
            "destroy": (IsOwnerOrReadOnlyOrAdmin(),),
        }
        return action_permissions.get(self.action, super().get_permissions())

    def get_serializer_class(self):
        """
        Получить сериализатор в зависимости от операции.
        :return: Класс сериализатора.
        """

        if self.action == "composition_basket":
            return ShoppingCartSummarySerializer
        return ShoppingCartProductSerializer

    def get_queryset(self):
        """
        Проверка queryset по текущему пользователю.
        :return: QuerySet, отфильтрованный по текущему пользователю.
        """

        user = self.request.user
        return (
            ShoppingCartProduct.objects.select_related("product_cart")
            .prefetch_related("product")
            .filter(product_cart__user=user)
        )

    def perform_create(self, serializer):
        """
        Добавляет продукт в корзину или обновляет (увеличивает) количество,
        если он уже в корзине.
        :param serializer: Сериализатор, содержащий данные о продукте и количестве.
        :return: Ответ с данными о добавленном/обновленном продукте.
        """

        try:
            user = self.request.user
            product_id = serializer.validated_data["product"].id
            amount = serializer.validated_data["amount"]

            product_cart, _ = ProductCart.objects.get_or_create(user=user)
            shopping_cart_product, created = ShoppingCartProduct.objects.get_or_create(
                product_cart=product_cart,
                product_id=product_id,
                defaults={"amount": amount},
            )

            if not created:
                shopping_cart_product.amount += amount
                shopping_cart_product.save()

            serializer = self.get_serializer(shopping_cart_product)
            return Response(
                {"message": "Продукт успешно добавлен/обновлен!", **serializer.data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """
        Обновляет данные о продукте в корзине.
        :param serializer: Сериализатор, содержащий данные о продукте.
        :return: Ответ с данными об обновленном продукте.
        """
        try:
            instance = serializer.instance
            serializer.validated_data.get("amount", instance.amount)
            serializer.save()

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        """
        Удаляет продукт из корзины.
        :param instance: Экземпляр продукта для удаления.
        :return: Ответ с сообщением об успешном удалении продукта.
        """

        try:
            instance_id = instance.id
            instance.delete()
            return Response(
                {"message": "Продукт успешно удален", "id": instance_id},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception:
            return Response(
                {"detail": "Такого продукта в корзине пользователя нет!"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=False,
        methods=["post"],
        url_path="reduce_product",
        permission_classes=(IsOwnerOrReadOnlyOrAdmin,),
    )
    def reduce_product(self, request):
        """
        Уменьшает количество продукта в корзине.
        :param request: Запрос, содержащий данные о продукте и количестве.
        :return: Ответ с сообщением об успешном уменьшении количества продукта.
        """

        product_id = request.data.get("product")
        amount = request.data.get("amount")

        try:
            product = ShoppingCartProduct.objects.get(product_id=product_id)
            if amount > 0:
                product.amount -= amount
                product.save()
                return Response(
                    {"message": "Количество продукта успешно уменьшено."}, status=200
                )
            else:
                return Response(
                    {"message": "Количество должно быть положительным числом."},
                    status=400,
                )
        except ShoppingCartProduct.DoesNotExist:
            return Response({"message": "Продукт не найден в корзине."}, status=404)

    @action(
        detail=False,
        methods=["get"],
        url_path="composition_basket_sum",
        permission_classes=(IsOwnerOrReadOnlyOrAdmin,),
    )
    def composition_basket_sum(self, request):
        """
        Выводит состав корзины с подсчетом количества товаров и
            суммы стоимости товаров в корзине.
        :param request: Запрос.
        :return: Ответ с данными о составе корзины,
            количестве товаров и сумме стоимости товаров.
        """

        user = request.user
        products = ShoppingCartProduct.objects.filter(
            product_cart__user=user
        ).values_list("product__name", flat=True)
        total_data = ShoppingCartProduct.objects.filter(
            product_cart__user=user
        ).aggregate(
            total_amount=Sum("amount"),
            total_price=Sum(F("amount") * F("product__price")),
        )
        data = {
            "Продукты": "; ".join(products) ,
            "Общее количество продуктов": total_data["total_amount"],
            "Общая сумма продуктов": f"{total_data['total_price']} рублей",
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["delete"],
        url_path="clear_product_cart",
        permission_classes=(IsOwnerOrReadOnlyOrAdmin,),
    )
    def clear_product_cart(self, request):
        """
        Полностью очищает продуктовую корзину у пользователя.
        :param request: Запрос.
        :return: Ответ с сообщением об успешной очистке корзины
            или сообщением об ошибке.
        """
        user = request.user
        try:
            product_cart = ProductCart.objects.get(user=user)
            product_cart.shopping_cart_products.all().delete()
            return Response(
                {"detail": "Корзина полностью очищена!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ProductCart.DoesNotExist:
            return Response(
                {"detail": "Корзина пользователя не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )
