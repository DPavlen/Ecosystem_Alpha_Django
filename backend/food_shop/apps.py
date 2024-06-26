from django.apps import AppConfig


class FoodShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "food_shop"

    def ready(self):
        """"
        Регистрируем сигналы при запуске app food_shop.
        """

        import food_shop.signals