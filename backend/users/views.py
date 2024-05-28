from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from users.models import MyUser
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    Кастомный ViewSet для работы с пользователями.
    Предоставляет эндпоинты для управления пользователями, включая активацию.
    Attributes:
        - queryset: Запрос, возвращающий все объекты пользователей.
        - serializer_class: Сериализатор, используемый для
        преобразования данных пользователя.
    Permissions:
        - permission_classes: Список классов разрешений для ViewSet.
        Здесь установлен AllowAny для открытого доступа.
    Methods:
        - activate(self, request, uid, token, format=None): Активирует
        пользователя с заданным UID и токеном.
    """

    queryset = MyUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == "list":
            return (IsAdminUser(),)
        return (AllowAny(),)

