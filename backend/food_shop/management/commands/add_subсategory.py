import json

from django.core.management.base import BaseCommand
from food_shop.models import Category, Subcategory


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open("data/subcategory.json", encoding="utf-8-sig") as f:
                subcategory_data = json.load(f)
                for subcategory in subcategory_data:
                    name = subcategory.get("name")
                    # Получаем связанный объект Category по id и связке с name
                    category_name = subcategory.get("category_name")
                    if category_name:
                        category, _ = Category.objects.get_or_create(name=category_name)
                        Subcategory.objects.get_or_create(
                            name=name,
                            category=category
                        )
        except Exception:
            raise ("Ошибка при загрузке Подкатегорий':")
        return (
            "Загрузка 'Подкатегорий' произошла успешно!"
            " Обработка файла subcategory.json завершена."
        )