from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import logging

from .models import Product


def resize_image(image, max_size):
    """
    Изменяет размер изображения, сохраняя его пропорции, так чтобы
    ни ширина, ни высота не превышали заданное максимальное значение.
    Параметры:
    image (File): Файл изображения, который нужно изменить.
    max_size (int): Максимальное значение для ширины и высоты изображения.
    Возвращает:
    None: Функция изменяет размер изображения на месте и сохраняет его
          в том же файле.
    """

    img = Image.open(image)
    img.thumbnail((max_size, max_size))
    img.save(image.path)


@receiver(post_save, sender=Product)
def resize_product_images(sender, instance, **kwargs):
    """
    Сигнал, изменяющий размер изображений продукта после его сохранения(post_save).

    Параметры:
    sender (Model): Модель, которая отправляет сигнал.
    instance (Product): Экземпляр модели, который был сохранен.
    **kwargs: Произвольные именованные аргументы.
    """

    print(f"Сигнал вызван для продукта: {instance.name}")
    if instance.icon_small:
        resize_image(instance.icon_small, 200)
    if instance.icon_middle:
        resize_image(instance.icon_middle, 400)
    if instance.icon_big:
        resize_image(instance.icon_big, 600)