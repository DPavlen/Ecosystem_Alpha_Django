from rest_framework import serializers

from food_shop.models import Category, Subcategory, Product, ShoppingCartProduct


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для подкатегорий товаров.
    Attributes:
        - id: Уникальный идентификатор подкатегории.
        - name: Название подкатегории.
        - slug: Слаг подкатегории.
        - category: Название связанной категории.
        - icon: Иконка подкатегории.
    """

    category = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ("id", "name", "slug", "category", "icon")

    @staticmethod
    def get_category(instance):
        """
        Получить название категории продукта.
        Parameters:
            instance (Subcategory): Экземпляр подкатегории.
        Returns:
            str: Название связанной категории.
        """
        return instance.category.name


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категорий товаров.
    Attributes:
        - id: Уникальный идентификатор категории.
        - name: Название категории.
        - slug: Слаг категории.
        - icon: Иконка категории.
    """

    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "icon",
            "subcategories",
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продуктов.
    Attributes:
        - id: Уникальный идентификатор продукта.
        - name: Название продукта.
        - slug: Слаг продукта.
        - subcategory: Связанная подкатегория продукта.
        - price: Стоимость продукта.
        - measurement_unit: Единица измерения продукта.
        - icon_small: Маленькая иконка продукта.
        - icon_middle: Средняя иконка продукта.
        - icon_big: Большая иконка продукта.
        - category: Название связанной категории.
    """

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
        """
        Получить название категории продукта.
        Parameters:
            instance (Product): Экземпляр продукта.
        Returns:
            str: Название связанной категории.
        """
        return instance.subcategory.category.name


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для товаров в корзине покупок.
    Attributes:
        - product: Связанный продукт.
        - amount: Количество товара.
        - total_price: Общая стоимость товара.
    """

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )
    amount = serializers.IntegerField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartProduct
        fields = (
            "product",
            "amount",
            "total_price")

    def get_total_price(self, instance):
        """
        Получить общую стоимость товара.
        Parameters:
            instance (ShoppingCartProduct): Экземпляр товара в корзине покупок.
        Returns:
            Общая стоимость товара.
        """

        return instance["product"].price * instance["amount"]


class ShoppingCartSummarySerializer(serializers.Serializer):
    """
    Сериализатор для сводной информации о корзине покупок.
    Attributes:
        - total_amount: Общее количество товаров.
        - total_price: Общая стоимость товаров.
    """

    total_amount = serializers.IntegerField()
    total_price = serializers.CharField()

    class Meta:
        model = ShoppingCartProduct
        fields = (
            "total_amount",
            "total_price",
        )
