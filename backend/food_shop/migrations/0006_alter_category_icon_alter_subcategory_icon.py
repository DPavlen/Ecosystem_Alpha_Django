# Generated by Django 5.0.2 on 2024-05-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("food_shop", "0005_alter_product_icon_big_alter_product_icon_middle_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="icon",
            field=models.ImageField(
                blank=True,
                default=None,
                upload_to="categories",
                verbose_name="Фото категории",
            ),
        ),
        migrations.AlterField(
            model_name="subcategory",
            name="icon",
            field=models.ImageField(
                blank=True,
                default=None,
                upload_to="subcategories",
                verbose_name="Фото подкатегории",
            ),
        ),
    ]