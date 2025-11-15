"""
Vistas de la API REST
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Game, Review, UserLibrary, Developer, Category
from .serializers import (
    GameSerializer, ReviewSerializer, UserLibrarySerializer,
    DeveloperSerializer, CategorySerializer
)


class GameViewSet(viewsets.ModelViewSet):
    """ViewSet para juegos"""
    queryset = Game.objects.select_related('developer').prefetch_related('categories').all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['developer', 'categories']
    search_fields = ['title', 'description', 'developer__name']
    ordering_fields = ['title', 'release_date', 'rating']
    ordering = ['-release_date']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_library(self, request, pk=None):
        """Agregar juego a la biblioteca del usuario"""
        game = self.get_object()
        library_item, created = UserLibrary.objects.get_or_create(
            user=request.user,
            game=game
        )
        if created:
            serializer = UserLibrarySerializer(library_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Juego ya está en tu biblioteca'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Obtener reseñas de un juego"""
        game = self.get_object()
        reviews = game.reviews.select_related('user').all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet para reseñas"""
    queryset = Review.objects.select_related('user', 'game').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['game', 'user', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserLibraryViewSet(viewsets.ModelViewSet):
    """ViewSet para biblioteca de usuario"""
    serializer_class = UserLibrarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserLibrary.objects.filter(user=self.request.user).select_related('game')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeveloperViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para desarrolladores (solo lectura)"""
    queryset = Developer.objects.annotate(game_count=Count('games')).all()
    serializer_class = DeveloperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'country']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para categorías (solo lectura)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

