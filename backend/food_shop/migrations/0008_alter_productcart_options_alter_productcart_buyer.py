# Generated by Django 5.0.2 on 2024-05-27 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("food_shop", "0007_alter_product_category_productcart"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="productcart",
            options={
                "ordering": ("date_create",),
                "verbose_name": "Продуктовая корзина",
                "verbose_name_plural": "Продуктовые корзины",
            },
        ),
        migrations.AlterField(
            model_name="productcart",
            name="buyer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь продуктовой корзины",
            ),
        ),
    ]