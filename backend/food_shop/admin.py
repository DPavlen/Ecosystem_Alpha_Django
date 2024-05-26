from django.contrib import admin

from food_shop.models import Category, Subcategory


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