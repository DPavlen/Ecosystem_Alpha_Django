from django.contrib import admin

from .models import MyUser


class BaseAdminSettings(admin.ModelAdmin):
    """
    Базовая настройка панели администратора.
    Attributes:
        - empty_value_display: Значение для отображения при пустом поле.
        - list_filter: Поля для фильтрации в списке объектов.
    """

    empty_value_display = "-пусто-"
    list_filter = ("email", "username")


@admin.register(MyUser)
class UsersAdmin(BaseAdminSettings):
    """
    Администратор пользователей.
    Предоставляет интерфейс для управления пользователями.
    Attributes:
        - inlines: Встраиваемые таблицы.
        - list_display: Поля для отображения в списке объектов.
        - list_display_links: Поля, являющиеся ссылками на детальную информацию.
        - search_fields: Поля, по которым доступен поиск.
    """

    list_display = (
        "id",
        "role",
        "username",
        "email",
    )
    list_display_links = ("id", "username")
    search_fields = ("username", "role")
