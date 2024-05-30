from django.db.models import Count, F
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated

from api.v1.serializers import (
    CategorySerializer,
    SubcategorySerializer,
    ProductSerializer,
    ShoppingCartProductSerializer)
#from core.pagination import PaginationCust
from food_shop.models import Category, Subcategory, Product, ShoppingCartProduct, ProductCart


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet для работы c категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = PaginationCust


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet для работы c подкатегориями."""
    queryset = Subcategory.objects.select_related("category")
    serializer_class = SubcategorySerializer
    # pagination_class = PaginationCust


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet для работы c продуктами."""
    queryset = Product.objects.select_related("subcategory").prefetch_related(
        "subcategory__category"
    )
    serializer_class = ProductSerializer
    # permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationCust


class ShoppingCartProductViewSet(viewsets.ModelViewSet):
    """Кастомный ViewSet  для работы с продуктовой корзиной."""
    queryset = ShoppingCartProduct.objects.all()
    serializer_class = ShoppingCartProductSerializer
    #permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationCust

    def get_permissions(self):
        """Возвращает соответствующие разрешения в зависимости от действия."""
        action_permissions = {
            "list": (permissions.AllowAny(),),
            "retrieve": (permissions.AllowAny(),),
            "create": (permissions.IsAuthenticated(),),
            "update": (permissions.IsAuthenticated(),),
            "partial_update": (permissions.IsAuthenticated(),),
            "destroy": (permissions.IsAuthenticated(),),
        }
        return action_permissions.get(self.action, super().get_permissions())

    def get_serializer_class(self):
        """Получить сериализатор."""
        return ShoppingCartProductSerializer

    def get_queryset(self):
        """Проверка queryset по текущему пользователю."""
        user = self.request.user
        return ShoppingCartProduct.objects.select_related(
            "product_cart"
        ).prefetch_related("product").filter(
            product_cart__user=user
        )

    def perform_create(self, serializer):
        """Добавляет продукт в корзину или обновляет количество, если он уже в корзине."""
        try:
            user = self.request.user
            product_id = serializer.validated_data['product'].id
            amount = serializer.validated_data['amount']

            product_cart, _ = ProductCart.objects.get_or_create(user=user)
            shopping_cart_product, created = ShoppingCartProduct.objects.get_or_create(
                product_cart=product_cart,
                product_id=product_id,
                defaults={'amount': amount}
            )

            if not created:
                shopping_cart_product.amount += amount
                shopping_cart_product.save()

            serializer = self.get_serializer(shopping_cart_product)
            return Response(
                {
                    "message": "Продукт успешно добавлен/обновлен!",
                    **serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """Обновляет данные о продукте в корзине."""
        try:
            instance = serializer.instance
            serializer.validated_data.get("amount", instance.amount)
            serializer.save()

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        """Удаляет продукт из корзины."""
        try:
            instance_id = instance.id
            instance.delete()
            return Response({
                "message": "Продукт успешно удален",
                "id": instance_id
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "detail": "Такого продукта в корзине пользователя нет!"
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"], url_path="composition_basket")
    def composition_basket(self, request):
        """Выводит состав корзины с подсчетом количества товаров
        и суммы стоимости товаров в корзине."""
        user = request.user
        shopping_cart = ShoppingCartProduct.objects.select_related(
            "product_cart"
        ).prefetch_related("product").filter(
            product_cart__user=user
        )
        total_amount = 0
        total_price = 0
        for item in shopping_cart:
            total_amount += item.amount
            total_price += item.product.price * item.amount

        data = {
            "total_amount": total_amount,
            "total_price": f"{total_price} рублей"
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="clear_product_cart")
    def clear_product_cart(self, request):
        """Полностью очищает продуктовую корзину у пользователя."""
        user = request.user
        try:
            product_cart = ProductCart.objects.get(user=user)
            product_cart.shopping_cart_products.all().delete()
            return Response(
                {"detail": "Корзина полностью очищена!"},
                status=status.HTTP_204_NO_CONTENT)
        except ProductCart.DoesNotExist:
            return Response(
                {"detail": "Корзина пользователя не найдена"},
                status=status.HTTP_404_NOT_FOUND)