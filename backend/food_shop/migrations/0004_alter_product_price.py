# Generated by Django 5.0.2 on 2024-06-02 11:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("food_shop", "0003_alter_subcategory_options_alter_category_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[
                    django.core.validators.MinValueValidator(
                        1,
                        message="Минимальное стоимость продукта должна быть не меньше 1.",
                    ),
                    django.core.validators.MaxValueValidator(
                        10000,
                        message="Максимальная стоимость продукта должна быть не больше 10000.",
                    ),
                ],
                verbose_name="Стоимость продукта",
            ),
        ),
    ]
