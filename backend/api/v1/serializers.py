from rest_framework import serializers
from rest_framework.fields import IntegerField

from core.constants import LenghtField
from food_shop.models import Category, Subcategory, Product, ProductCart, ShoppingCartProduct
from users.serializers import CustomUserSerializer


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
    subcategory = SubcategorySerializer(read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "subcategory",
            "price",
            "measurement_unit",
            "icon_small",
            "icon_middle",
            "icon_big",
            "category",
        )

    @staticmethod
    def get_category(instance):
        """Получить название категории продукта."""
        return instance.subcategory.category.name


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )
    amount = serializers.IntegerField(
    )
    #name = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartProduct
        fields = (
            #"product_id",
            "product",
            #"name",
            "amount",
            "total_price"
        )

    # def get_name(self, instance):
    #     return instance.product.name

    def get_total_price(self, instance):
        return instance['product'].price * instance['amount']



class ShoppingCartSummarySerializer(serializers.Serializer):
    total_amount = serializers.IntegerField()
    total_price = serializers.CharField()

    class Meta:
        model = ShoppingCartProduct
        fields = (
            "total_amount",
            "total_price",
        )
