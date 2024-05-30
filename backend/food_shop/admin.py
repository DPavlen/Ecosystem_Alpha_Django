from django.contrib import admin
from django.utils.html import format_html

from food_shop.models import Category, Subcategory, Product, ProductCart, ShoppingCartProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настроенная панель админки категории товара."""
    list_display = ("pk", "name", "slug")
    search_fields = ("name", "slug")
    empty_value_display = "-пусто-"


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Настроенная панель админки подкатегории товара."""
    list_display = ("pk", "name", "slug", "category",)
    search_fields = ("name", "slug")
    list_filter = ("category",)
    empty_value_display = "-пусто-"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настроенная панель админки продуктов."""
    list_display = (
        "pk",
        "name",
        "date_add",
        "slug",
        "subcategory",
        "price",
        "measurement_unit",
        "icon_small",
        "icon_middle",
        "icon_big"
    )
    search_fields = ("name", "slug", "date_add", "price", "measurement_unit")
    list_filter = ("name", "subcategory", "price")
    empty_value_display = "-пусто-"

    def display_icon(self, obj, field_name):
        """
        Возвращает отображение иконки категории по указанному полю.
        Args: obj (Category): Объект категории.
              field_name (str): Имя поля с изображением.
        Returns: str: HTML-код для отображения изображения.
        """
        image = getattr(obj, field_name)
        if image:
            return format_html(
                '<img src="{}" style="max-width:100px; max-height:100px"/>'.format(image.url)
            )
        return "-"

    def display_icon_small(self, obj):
        return self.display_icon(obj, 'icon_small')

    def display_icon_middle(self, obj):
        return self.display_icon(obj, 'icon_middle')

    def display_icon_big(self, obj):
        return self.display_icon(obj, 'icon_big')

    display_icon_small.short_description = 'Icon Small'
    display_icon_middle.short_description = 'Icon Middle'
    display_icon_big.short_description = 'Icon Big'

    def formatted_date_add(self, obj):
        return obj.date_add.strftime("%B %d, %Y, %I:%M %p")

    formatted_date_add.short_description = "Дата добавления продукта"


@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    """Настроенная панель админки продуктовой корзины."""
    list_display = ("pk", "user", "date_created",)
    search_fields = ("user", "date_created",)
    list_filter = ("user", "date_created",)
    empty_value_display = "-пусто-"

    def formatted_date_created(self, obj):
        return obj.date_created.strftime("%B %d, %Y, %I:%M %p")

    formatted_date_created.short_description = "Дата создания корзины"


@admin.register(ShoppingCartProduct)
class ShoppingCartProductAdmin(admin.ModelAdmin):
    """Настроенная панель админки продуктовой корзины товаров."""
    list_display = ("pk", "product_cart", "product", "amount", "date_created")
    search_fields = ("pk", "product_cart", "product", "amount", "date_created")
    list_filter = ("product_cart", "product",)
    empty_value_display = "-пусто-"