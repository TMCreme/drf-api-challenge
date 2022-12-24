"""
URLs for API access
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewset


router = DefaultRouter()

router.register("post", PostViewset)

app_name = "post"

urlpatterns = [
    path("", include(router.urls)),
]
