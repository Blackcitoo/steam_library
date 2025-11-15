"""
Vistas para la aplicación de Biblioteca de Steam
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Count, Avg, Sum
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import csv
from .models import Game, Review, UserLibrary, Developer, Category, Notification
from .forms import CustomUserCreationForm, GameForm, ReviewForm, UserLibraryForm, SearchForm


# ==================== VISTAS DE AUTENTICACIÓN ====================

def register_view(request):
    """Vista de registro de usuarios"""
    if request.user.is_authenticated:
        return redirect('library:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente.')
            return redirect('library:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'library/register.html', {'form': form})


# ==================== VISTAS PRINCIPALES ====================

class GameListView(ListView):
    """Lista de juegos con búsqueda y filtros"""
    model = Game
    template_name = 'library/game_list.html'
    context_object_name = 'games'
    paginate_by = 12

    def get_queryset(self):
        queryset = Game.objects.select_related('developer').prefetch_related('categories').all()
        
        # Búsqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(developer__name__icontains=query)
            )
        
        # Filtro por categoría
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        
        # Filtro por calificación mínima
        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        
        # Ordenamiento
        order_by = self.request.GET.get('order_by', '-release_date')
        if order_by in ['title', '-title', 'rating', '-rating', 'release_date', '-release_date']:
            queryset = queryset.order_by(order_by)
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(game_count=Count('games')).order_by('-game_count')[:10]
        context['search_form'] = SearchForm(self.request.GET)
        context['total_games'] = Game.objects.count()
        return context


class GameDetailView(DetailView):
    """Detalle de un juego"""
    model = Game
    template_name = 'library/game_detail.html'
    context_object_name = 'game'

    def get_queryset(self):
        return Game.objects.select_related('developer').prefetch_related('categories', 'reviews__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        
        # Reseñas paginadas
        reviews = game.reviews.select_related('user').order_by('-created_at')
        paginator = Paginator(reviews, 5)
        page = self.request.GET.get('page')
        context['reviews'] = paginator.get_page(page)
        
        # Estadísticas
        context['avg_rating'] = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        context['total_reviews'] = reviews.count()
        
        # Verificar si el usuario tiene el juego en su biblioteca
        if self.request.user.is_authenticated:
            context['in_library'] = UserLibrary.objects.filter(
                user=self.request.user, 
                game=game
            ).exists()
            context['user_review'] = Review.objects.filter(
                user=self.request.user,
                game=game
            ).first()
        
        return context


@login_required
def add_to_library(request, pk):
    """Agregar juego a la biblioteca del usuario"""
    game = get_object_or_404(Game, pk=pk)
    library_item, created = UserLibrary.objects.get_or_create(
        user=request.user,
        game=game
    )
    
    if created:
        messages.success(request, f'"{game.title}" ha sido agregado a tu biblioteca.')
        # Crear notificación
        Notification.objects.create(
            user=request.user,
            notification_type='game',
            title='Juego agregado',
            message=f'Has agregado "{game.title}" a tu biblioteca.'
        )
    else:
        messages.info(request, f'"{game.title}" ya está en tu biblioteca.')
    
    return redirect('library:game_detail', pk=pk)


@login_required
def remove_from_library(request, pk):
    """Remover juego de la biblioteca"""
    game = get_object_or_404(Game, pk=pk)
    UserLibrary.objects.filter(user=request.user, game=game).delete()
    messages.success(request, f'"{game.title}" ha sido removido de tu biblioteca.')
    return redirect('library:my_library')


# ==================== VISTAS CRUD PARA JUEGOS ====================

class GameCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Crear nuevo juego (solo staff)"""
    model = Game
    form_class = GameForm
    template_name = 'library/game_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Juego creado exitosamente.')
        return super().form_valid(form)


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Actualizar juego (solo staff)"""
    model = Game
    form_class = GameForm
    template_name = 'library/game_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Juego actualizado exitosamente.')
        return super().form_valid(form)


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar juego (solo staff)"""
    model = Game
    template_name = 'library/game_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Juego eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ==================== VISTAS CRUD PARA RESEÑAS ====================

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva reseña"""
    model = Review
    form_class = ReviewForm
    template_name = 'library/review_form.html'

    def form_valid(self, form):
        game = get_object_or_404(Game, pk=self.kwargs['game_pk'])
        form.instance.user = self.request.user
        form.instance.game = game
        
        # Verificar si ya existe una reseña
        if Review.objects.filter(user=self.request.user, game=game).exists():
            messages.error(self.request, 'Ya has publicado una reseña para este juego.')
            return redirect('library:game_detail', pk=game.pk)
        
        messages.success(self.request, 'Reseña publicada exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.game.get_absolute_url()


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Actualizar reseña"""
    model = Review
    form_class = ReviewForm
    template_name = 'library/review_form.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def form_valid(self, form):
        messages.success(self.request, 'Reseña actualizada exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.game.get_absolute_url()


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar reseña"""
    model = Review
    template_name = 'library/review_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return self.object.game.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Reseña eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ==================== VISTAS DE BIBLIOTECA ====================

@login_required
def my_library_view(request):
    """Vista de la biblioteca del usuario"""
    library_items = UserLibrary.objects.filter(user=request.user).select_related('game', 'game__developer')
    
    # Filtros
    favorite_only = request.GET.get('favorite')
    if favorite_only:
        library_items = library_items.filter(is_favorite=True)
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        library_items = library_items.filter(
            Q(game__title__icontains=query) |
            Q(game__description__icontains=query)
        )
    
    # Ordenamiento
    order_by = request.GET.get('order_by', '-date_added')
    if order_by in ['game__title', '-game__title', 'hours_played', '-hours_played', 
                    'date_added', '-date_added', 'last_played', '-last_played']:
        library_items = library_items.order_by(order_by)
    
    # Paginación
    paginator = Paginator(library_items, 12)
    page = request.GET.get('page')
    library_items = paginator.get_page(page)
    
    return render(request, 'library/my_library.html', {
        'library_items': library_items,
        'total_games': UserLibrary.objects.filter(user=request.user).count(),
        'total_hours': UserLibrary.objects.filter(user=request.user).aggregate(
            total=Sum('hours_played')
        )['total'] or 0,
    })


@login_required
def update_library_item(request, pk):
    """Actualizar item de la biblioteca"""
    library_item = get_object_or_404(UserLibrary, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = UserLibraryForm(request.POST, instance=library_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Biblioteca actualizada exitosamente.')
            return redirect('library:my_library')
    else:
        form = UserLibraryForm(instance=library_item)
    
    return render(request, 'library/update_library_item.html', {
        'form': form,
        'library_item': library_item
    })


# ==================== VISTAS ADICIONALES ====================

def home_view(request):
    """Vista principal"""
    featured_games = Game.objects.select_related('developer').order_by('-rating')[:6]
    recent_games = Game.objects.select_related('developer').order_by('-release_date')[:6]
    popular_games = Game.objects.select_related('developer').annotate(
        review_count=Count('reviews')
    ).order_by('-review_count')[:6]
    
    context = {
        'featured_games': featured_games,
        'recent_games': recent_games,
        'popular_games': popular_games,
    }
    
    if request.user.is_authenticated:
        context['my_library_count'] = UserLibrary.objects.filter(user=request.user).count()
    
    return render(request, 'library/home.html', context)


@login_required
def user_profile_view(request, pk):
    """Perfil de usuario"""
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    library_count = UserLibrary.objects.filter(user=user).count()
    reviews_count = Review.objects.filter(user=user).count()
    total_hours = UserLibrary.objects.filter(user=user).aggregate(
        total=Sum('hours_played')
    )['total'] or 0
    
    return render(request, 'library/user_profile.html', {
        'profile_user': user,
        'library_count': library_count,
        'reviews_count': reviews_count,
        'total_hours': total_hours,
    })


class DeveloperListView(ListView):
    """Lista de desarrolladores"""
    model = Developer
    template_name = 'library/developer_list.html'
    context_object_name = 'developers'
    paginate_by = 12

    def get_queryset(self):
        queryset = Developer.objects.annotate(game_count=Count('games'))
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset.order_by('-game_count')


class DeveloperDetailView(DetailView):
    """Detalle de desarrollador"""
    model = Developer
    template_name = 'library/developer_detail.html'
    context_object_name = 'developer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        developer = self.get_object()
        games = developer.games.all()
        paginator = Paginator(games, 12)
        page = self.request.GET.get('page')
        context['games'] = paginator.get_page(page)
        return context


@login_required
def notifications_view(request):
    """Vista de notificaciones"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(notifications, 10)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    
    return render(request, 'library/notifications.html', {
        'notifications': notifications
    })


@login_required
@require_http_methods(["POST"])
def mark_notification_read(request, pk):
    """Marcar notificación como leída"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'ok'})


# ==================== EXPORTAR DATOS ====================

@login_required
def export_library_csv(request):
    """Exportar biblioteca a CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mi_biblioteca.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Juego', 'Desarrollador', 'Horas Jugadas', 'Favorito', 'Fecha Agregado'])
    
    library_items = UserLibrary.objects.filter(user=request.user).select_related('game', 'game__developer')
    for item in library_items:
        writer.writerow([
            item.game.title,
            item.game.developer.name if item.game.developer else 'N/A',
            item.hours_played,
            'Sí' if item.is_favorite else 'No',
            item.date_added.strftime('%Y-%m-%d')
        ])
    
    return response

