from django.contrib import admin

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
    list_display = ("pk", "name", "date_add", "slug", "category", "price")
    search_fields = ("name", "slug", "date_add", "price")
    list_filter = ("name","category", "price")
    empty_value_display = "-пусто-"

    def formatted_date_add(self, obj):
        return obj.date_add.strftime("%B %d, %Y, %I:%M %p")

    formatted_date_add.short_description = "Дата добавления продукта"


@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    """Настроенная панель админки продуктовой корзины."""
    list_display = ("pk", "buyer", "date_create",)
    search_fields = ("buyer", "buyer", "date_create",)
    list_filter = ("buyer", "date_create",)
    empty_value_display = "-пусто-"

    def formatted_date_create(self, obj):
        return obj.date_create.strftime("%B %d, %Y, %I:%M %p")

    formatted_date_create.short_description = "Дата создания корзины"


@admin.register(ShoppingCartProduct)
class ShoppingCartProductAdmin(admin.ModelAdmin):
    """Настроенная панель админки продуктовой корзины товаров."""
    list_display = ("pk", "product_cart", "product", "amount")
    search_fields = ("pk", "product_cart", "product", "amount")
    list_filter = ("product_cart", "product",)
    empty_value_display = "-пусто-"