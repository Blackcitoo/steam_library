"""
Modelos para la aplicación de Biblioteca de Steam
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    """Modelo de usuario personalizado"""
    bio = models.TextField(max_length=500, blank=True, verbose_name='Biografía')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    steam_profile = models.URLField(blank=True, null=True, verbose_name='Perfil de Steam')
    is_premium = models.BooleanField(default=False, verbose_name='Usuario Premium')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('library:user_profile', kwargs={'pk': self.pk})


class Developer(models.Model):
    """Modelo para desarrolladores de juegos"""
    name = models.CharField(max_length=200, verbose_name='Nombre')
    country = models.CharField(max_length=100, blank=True, verbose_name='País')
    website = models.URLField(blank=True, null=True, verbose_name='Sitio web')
    description = models.TextField(blank=True, verbose_name='Descripción')
    logo = models.ImageField(upload_to='developers/', blank=True, null=True, verbose_name='Logo')

    class Meta:
        verbose_name = 'Desarrollador'
        verbose_name_plural = 'Desarrolladores'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('library:developer_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    """Modelo para categorías de juegos"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icono')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name


class Game(models.Model):
    """Modelo principal para juegos"""
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    release_date = models.DateField(verbose_name='Fecha de lanzamiento')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    cover_image = models.ImageField(upload_to='games/', blank=True, null=True, verbose_name='Portada')
    steam_url = models.URLField(blank=True, null=True, verbose_name='URL de Steam')
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, 
                                  related_name='games', verbose_name='Desarrollador')
    categories = models.ManyToManyField(Category, related_name='games', verbose_name='Categorías')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                                validators=[MinValueValidator(0), MaxValueValidator(5)],
                                verbose_name='Calificación promedio')
    total_reviews = models.IntegerField(default=0, verbose_name='Total de reseñas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'
        ordering = ['-release_date', 'title']
        indexes = [
            models.Index(fields=['-release_date']),
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('library:game_detail', kwargs={'pk': self.pk})

    def update_rating(self):
        """Actualiza la calificación promedio del juego"""
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.total_reviews = reviews.count()
            self.save(update_fields=['rating', 'total_reviews'])


class UserLibrary(models.Model):
    """Modelo para la biblioteca de juegos de cada usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library',
                            verbose_name='Usuario')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='in_libraries',
                            verbose_name='Juego')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de adición')
    hours_played = models.DecimalField(max_digits=6, decimal_places=2, default=0.00,
                                      validators=[MinValueValidator(0)],
                                      verbose_name='Horas jugadas')
    is_favorite = models.BooleanField(default=False, verbose_name='Favorito')
    last_played = models.DateTimeField(null=True, blank=True, verbose_name='Última vez jugado')

    class Meta:
        verbose_name = 'Biblioteca de Usuario'
        verbose_name_plural = 'Bibliotecas de Usuarios'
        unique_together = ['user', 'game']
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['user', '-date_added']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"


class Review(models.Model):
    """Modelo para reseñas de juegos"""
    RATING_CHOICES = [
        (1, '1 - Muy Malo'),
        (2, '2 - Malo'),
        (3, '3 - Regular'),
        (4, '4 - Bueno'),
        (5, '5 - Excelente'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews',
                            verbose_name='Usuario')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews',
                            verbose_name='Juego')
    rating = models.IntegerField(choices=RATING_CHOICES, 
                                validators=[MinValueValidator(1), MaxValueValidator(5)],
                                verbose_name='Calificación')
    comment = models.TextField(verbose_name='Comentario')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    is_helpful = models.IntegerField(default=0, verbose_name='Útil')

    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        unique_together = ['user', 'game']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['game', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating}/5)"

    def save(self, *args, **kwargs):
        """Actualiza la calificación del juego al guardar"""
        super().save(*args, **kwargs)
        self.game.update_rating()

    def delete(self, *args, **kwargs):
        """Actualiza la calificación del juego al eliminar"""
        game = self.game
        super().delete(*args, **kwargs)
        game.update_rating()


class Notification(models.Model):
    """Modelo para notificaciones del sistema"""
    NOTIFICATION_TYPES = [
        ('review', 'Nueva Reseña'),
        ('game', 'Nuevo Juego'),
        ('friend', 'Amigo'),
        ('system', 'Sistema'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',
                            verbose_name='Usuario')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES,
                                        verbose_name='Tipo')
    title = models.CharField(max_length=200, verbose_name='Título')
    message = models.TextField(verbose_name='Mensaje')
    is_read = models.BooleanField(default=False, verbose_name='Leída')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    link = models.URLField(blank=True, null=True, verbose_name='Enlace')

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

