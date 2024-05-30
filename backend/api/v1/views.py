from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.v1.serializers import (
    CategorySerializer, SubcategorySerializer, ProductSerializer, ProductCartSerializer, ShoppingCartProductSerializer)
#from core.pagination import PaginationCust
from food_shop.models import Category, Subcategory, Product, ShoppingCartProduct


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
    permission_classes = (IsAuthenticated,)
    # pagination_class = PaginationCust

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