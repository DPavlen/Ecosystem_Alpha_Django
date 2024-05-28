from rest_framework import serializers
from rest_framework.fields import IntegerField

from food_shop.models import Category, Subcategory, Product


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий товаров."""
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "icon",
        )


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий товаров."""
    category = serializers.SerializerMethodField()
    #category = serializers.CharField()


    class Meta:
        model = Subcategory
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "icon"
        )

    @staticmethod
    def get_category(instance):
       """Получить название категории продукта."""
       return instance.category.name


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов."""
    category = serializers.SerializerMethodField()
    subcategory = SubcategorySerializer()
    #icons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "subcategory",
            "price",
            "icon_small",
            "icon_middle",
            "icon_big",
        )

    @staticmethod
    def get_category(instance):
        """Получить название категории продукта."""
        return instance.subcategory.category.name