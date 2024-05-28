from django.urls import include, path
from rest_framework import routers

from api.v1.views import CategoryViewSet, SubcategoryViewSet, ProductViewSet

app_name = "api.v1"

router = routers.DefaultRouter()

router.register(r"category", CategoryViewSet, basename="category")
router.register(r"subcategory", SubcategoryViewSet, basename="subcategory")
router.register(r"product", ProductViewSet, basename="product")



urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]