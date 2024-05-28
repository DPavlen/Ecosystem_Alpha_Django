from django.db.models import Count, F
from rest_framework import viewsets

from api.v1.serializers import (
    CategorySerializer, SubcategorySerializer, ProductSerializer)
#from core.pagination import PaginationCust
from food_shop.models import Category, Subcategory, Product


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet для работы c категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = PaginationCust


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet для работы c подкатегориями."""
    queryset = Subcategory.objects.select_related("category")
    #queryset = Subcategory.objects.annotate(category_name=F("category__name"))
    serializer_class = SubcategorySerializer
    # pagination_class = PaginationCust


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Кастомный ViewSet для работы c продуктами."""
    queryset = Product.objects.select_related("subcategory").prefetch_related(
        "subcategory__category"
    )
    serializer_class = ProductSerializer
    # pagination_class = PaginationCust