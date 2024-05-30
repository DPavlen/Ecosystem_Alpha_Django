from rest_framework import serializers
from rest_framework.fields import IntegerField

from food_shop.models import Category, Subcategory, Product, ProductCart, ShoppingCartProduct


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
    subcategory = SubcategorySerializer()

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
        )


class ProductCartSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка продуктов в корзине."""
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartProduct
        fields = (
            "product",
            "amount",
            "total_price",
            "date_created"
        )

    @staticmethod
    def get_total_price(instance):
        """Возвращает общую стоимость каждого продукта в корзине."""
        return instance.product.price * instance.amount


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartProduct
        fields = (
            "product_cart",
            "product",
            "amount",
            "total_price"
        )

    def get_total_price(self, instance):
        return f"{instance.product.price * instance.amount} рублей"
