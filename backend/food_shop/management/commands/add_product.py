import json

from django.core.management.base import BaseCommand
from food_shop.models import Product, Subcategory


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            with open("data/product.json", encoding="utf-8-sig") as f:
                product_data = json.load(f)
                for product in product_data:
                    name = product.get("name")
                    price = product.get("price")
                    measurement_unit = product.get("measurement_unit")
                    # Получаем связанный объект Subcategory по id и связке с name
                    subcategory_name = product.get("subcategory_name")
                    if subcategory_name:
                        subcategory, _ = Subcategory.objects.get_or_create(name=subcategory_name)
                        Product.objects.get_or_create(
                            name=name,
                            price=price,
                            measurement_unit=measurement_unit,
                            subcategory=subcategory
                        )
        except Exception:
            raise ("Ошибка при загрузке Продуктов':")
        return (
            "Загрузка 'Продуктов' произошла успешно!"
            " Обработка файла product.json завершена."
        )