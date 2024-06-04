import json

from django.core.management.base import BaseCommand
from food_shop.models import Category


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open("data/category.json", encoding="utf-8-sig") as f:
                category_data = json.load(f)
                for category in category_data:
                    name = category.get("name")
                    Category.objects.get_or_create(name=name)
        except Exception:
            raise ("Ошибка при загрузке Категорий':")
        return (
            "Загрузка 'Категорий' произошла успешно!"
            " Обработка файла category.json завершена."
        )