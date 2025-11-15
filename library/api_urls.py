"""
URLs para la API REST
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    GameViewSet, ReviewViewSet, UserLibraryViewSet,
    DeveloperViewSet, CategoryViewSet
)

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'library', UserLibraryViewSet, basename='library')
router.register(r'developers', DeveloperViewSet, basename='developer')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]

