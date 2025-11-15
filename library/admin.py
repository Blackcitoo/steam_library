"""
Configuración del panel de administración personalizado
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, Game, Developer, Category, UserLibrary, Review, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para usuarios"""
    list_display = ['username', 'email', 'is_premium', 'date_joined', 'avatar_preview']
    list_filter = ['is_premium', 'is_staff', 'is_superuser', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('bio', 'avatar', 'steam_profile', 'is_premium')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('bio', 'avatar', 'steam_profile', 'is_premium')
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "Sin avatar"
    avatar_preview.short_description = 'Avatar'


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    """Admin para desarrolladores"""
    list_display = ['name', 'country', 'website', 'game_count', 'logo_preview']
    list_filter = ['country']
    search_fields = ['name', 'country']
    readonly_fields = ['logo_preview']

    def game_count(self, obj):
        return obj.games.count()
    game_count.short_description = 'Juegos'

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" />', obj.logo.url)
        return "Sin logo"
    logo_preview.short_description = 'Logo'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin para categorías"""
    list_display = ['name', 'game_count', 'icon']
    search_fields = ['name']

    def game_count(self, obj):
        return obj.games.count()
    game_count.short_description = 'Juegos'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Admin personalizado para juegos"""
    list_display = ['title', 'developer', 'release_date', 'price', 'rating', 
                   'total_reviews', 'cover_preview', 'created_at']
    list_filter = ['release_date', 'developer', 'categories', 'created_at']
    search_fields = ['title', 'description', 'developer__name']
    readonly_fields = ['rating', 'total_reviews', 'created_at', 'updated_at', 'cover_preview']
    filter_horizontal = ['categories']
    date_hierarchy = 'release_date'
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'description', 'cover_image', 'cover_preview')
        }),
        ('Detalles', {
            'fields': ('developer', 'categories', 'release_date', 'price', 'steam_url')
        }),
        ('Estadísticas', {
            'fields': ('rating', 'total_reviews', 'created_at', 'updated_at')
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="200" />', obj.cover_image.url)
        return "Sin portada"
    cover_preview.short_description = 'Vista previa'


@admin.register(UserLibrary)
class UserLibraryAdmin(admin.ModelAdmin):
    """Admin para bibliotecas de usuarios"""
    list_display = ['user', 'game', 'hours_played', 'is_favorite', 'date_added', 'last_played']
    list_filter = ['is_favorite', 'date_added']
    search_fields = ['user__username', 'game__title']
    readonly_fields = ['date_added']
    date_hierarchy = 'date_added'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin para reseñas"""
    list_display = ['user', 'game', 'rating', 'created_at', 'is_helpful']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'game__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin para notificaciones"""
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


# Personalización del sitio admin
admin.site.site_header = "Administración de Biblioteca Steam"
admin.site.site_title = "Biblioteca Steam Admin"
admin.site.index_title = "Panel de Control"

