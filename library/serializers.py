"""
Serializers para la API REST
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Game, Review, UserLibrary, Developer, Category

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']


class DeveloperSerializer(serializers.ModelSerializer):
    """Serializer para desarrolladores"""
    game_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Developer
        fields = ['id', 'name', 'country', 'website', 'description', 'logo', 'game_count']


class GameSerializer(serializers.ModelSerializer):
    """Serializer para juegos"""
    developer_name = serializers.CharField(source='developer.name', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'release_date', 'price', 'cover_image',
                 'steam_url', 'developer', 'developer_name', 'categories', 'rating',
                 'total_reviews', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer para reseñas"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    game_title = serializers.CharField(source='game.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'user_username', 'game', 'game_title', 'rating',
                 'comment', 'created_at', 'updated_at', 'is_helpful']
        read_only_fields = ['user', 'created_at', 'updated_at']


class UserLibrarySerializer(serializers.ModelSerializer):
    """Serializer para biblioteca de usuario"""
    game_title = serializers.CharField(source='game.title', read_only=True)
    game_cover = serializers.ImageField(source='game.cover_image', read_only=True)
    
    class Meta:
        model = UserLibrary
        fields = ['id', 'user', 'game', 'game_title', 'game_cover', 'date_added',
                 'hours_played', 'is_favorite', 'last_played']
        read_only_fields = ['user', 'date_added']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuarios"""
    library_count = serializers.IntegerField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'steam_profile',
                 'is_premium', 'date_joined', 'library_count', 'reviews_count']
        read_only_fields = ['date_joined']

