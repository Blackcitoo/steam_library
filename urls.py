"""
URLs para la aplicación library
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'library'

urlpatterns = [
    # Autenticación
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Páginas principales
    path('', views.home_view, name='home'),
    
    # Juegos
    path('games/', views.GameListView.as_view(), name='game_list'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('games/add/', views.GameCreateView.as_view(), name='game_create'),
    path('games/<int:pk>/edit/', views.GameUpdateView.as_view(), name='game_update'),
    path('games/<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    path('games/<int:pk>/add-to-library/', views.add_to_library, name='add_to_library'),
    path('games/<int:pk>/remove-from-library/', views.remove_from_library, name='remove_from_library'),
    
    # Reseñas
    path('games/<int:game_pk>/review/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    
    # Biblioteca
    path('my-library/', views.my_library_view, name='my_library'),
    path('my-library/<int:pk>/update/', views.update_library_item, name='update_library_item'),
    path('my-library/export/', views.export_library_csv, name='export_library_csv'),
    
    # Desarrolladores
    path('developers/', views.DeveloperListView.as_view(), name='developer_list'),
    path('developers/<int:pk>/', views.DeveloperDetailView.as_view(), name='developer_detail'),
    
    # Usuarios
    path('users/<int:pk>/', views.user_profile_view, name='user_profile'),
    
    # Notificaciones
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
]

