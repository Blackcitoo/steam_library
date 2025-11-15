"""
Tests para la aplicación library
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Game, Developer, Category, UserLibrary, Review, Notification

User = get_user_model()


class UserModelTest(TestCase):
    """Tests para el modelo User"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')


class GameModelTest(TestCase):
    """Tests para el modelo Game"""
    
    def setUp(self):
        self.developer = Developer.objects.create(
            name='Test Developer',
            country='USA'
        )
        self.category = Category.objects.create(name='Action')
        self.game = Game.objects.create(
            title='Test Game',
            description='A test game',
            release_date='2024-01-01',
            price=29.99,
            developer=self.developer
        )
        self.game.categories.add(self.category)
    
    def test_game_creation(self):
        self.assertEqual(self.game.title, 'Test Game')
        self.assertEqual(self.game.developer, self.developer)
        self.assertIn(self.category, self.game.categories.all())
    
    def test_game_str(self):
        self.assertEqual(str(self.game), 'Test Game')
    
    def test_update_rating(self):
        user = User.objects.create_user(username='user1', password='pass')
        Review.objects.create(
            user=user,
            game=self.game,
            rating=5,
            comment='Great game'
        )
        self.game.update_rating()
        self.assertEqual(self.game.rating, 5.0)
        self.assertEqual(self.game.total_reviews, 1)


class ReviewModelTest(TestCase):
    """Tests para el modelo Review"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.developer = Developer.objects.create(name='Dev')
        self.game = Game.objects.create(
            title='Game',
            description='Desc',
            release_date='2024-01-01',
            price=19.99,
            developer=self.developer
        )
    
    def test_review_creation(self):
        review = Review.objects.create(
            user=self.user,
            game=self.game,
            rating=4,
            comment='Good game'
        )
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.game, self.game)


class UserLibraryModelTest(TestCase):
    """Tests para el modelo UserLibrary"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.developer = Developer.objects.create(name='Dev')
        self.game = Game.objects.create(
            title='Game',
            description='Desc',
            release_date='2024-01-01',
            price=19.99,
            developer=self.developer
        )
    
    def test_library_creation(self):
        library_item = UserLibrary.objects.create(
            user=self.user,
            game=self.game,
            hours_played=10.5
        )
        self.assertEqual(library_item.hours_played, 10.5)
        self.assertEqual(library_item.user, self.user)
        self.assertEqual(library_item.game, self.game)


class AuthenticationTest(TestCase):
    """Tests de autenticación"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login(self):
        response = self.client.post(reverse('library:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('library:logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_register(self):
        response = self.client.post(reverse('library:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'bio': 'Test bio'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username='newuser').exists())


class GameViewsTest(TestCase):
    """Tests para las vistas de juegos"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staff',
            password='testpass123',
            is_staff=True
        )
        self.developer = Developer.objects.create(name='Test Dev')
        self.game = Game.objects.create(
            title='Test Game',
            description='Description',
            release_date='2024-01-01',
            price=29.99,
            developer=self.developer
        )
    
    def test_game_list_view(self):
        response = self.client.get(reverse('library:game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')
    
    def test_game_detail_view(self):
        response = self.client.get(reverse('library:game_detail', args=[self.game.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')
    
    def test_game_create_requires_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('library:game_create'))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_game_create_allows_staff(self):
        self.client.login(username='staff', password='testpass123')
        response = self.client.get(reverse('library:game_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_add_to_library(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('library:add_to_library', args=[self.game.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserLibrary.objects.filter(user=self.user, game=self.game).exists())


class ReviewViewsTest(TestCase):
    """Tests para las vistas de reseñas"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.developer = Developer.objects.create(name='Dev')
        self.game = Game.objects.create(
            title='Game',
            description='Desc',
            release_date='2024-01-01',
            price=19.99,
            developer=self.developer
        )
    
    def test_review_create(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('library:review_create', args=[self.game.pk]), {
            'rating': 5,
            'comment': 'Great game!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, game=self.game).exists())
    
    def test_review_update_own_review(self):
        self.client.login(username='testuser', password='testpass123')
        review = Review.objects.create(
            user=self.user,
            game=self.game,
            rating=3,
            comment='Original'
        )
        response = self.client.post(reverse('library:review_update', args=[review.pk]), {
            'rating': 5,
            'comment': 'Updated'
        })
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.comment, 'Updated')


class LibraryViewsTest(TestCase):
    """Tests para las vistas de biblioteca"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.developer = Developer.objects.create(name='Dev')
        self.game = Game.objects.create(
            title='Game',
            description='Desc',
            release_date='2024-01-01',
            price=19.99,
            developer=self.developer
        )
        self.library_item = UserLibrary.objects.create(
            user=self.user,
            game=self.game,
            hours_played=10.0
        )
    
    def test_my_library_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('library:my_library'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Game')
    
    def test_export_library_csv(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('library:export_library_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')


class APITest(TestCase):
    """Tests para la API REST"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.developer = Developer.objects.create(name='Dev')
        self.game = Game.objects.create(
            title='API Game',
            description='Desc',
            release_date='2024-01-01',
            price=19.99,
            developer=self.developer
        )
    
    def test_game_list_api(self):
        response = self.client.get('/api/games/')
        self.assertEqual(response.status_code, 200)
    
    def test_game_detail_api(self):
        response = self.client.get(f'/api/games/{self.game.pk}/')
        self.assertEqual(response.status_code, 200)
    
    def test_review_create_api(self):
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=self.user)
        response = self.client.post(
            '/api/reviews/',
            {
                'game': self.game.pk,
                'rating': 5,
                'comment': 'API review'
            },
            HTTP_AUTHORIZATION=f'Token {token.key}'
        )
        self.assertEqual(response.status_code, 201)


class NotificationTest(TestCase):
    """Tests para notificaciones"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
    
    def test_notification_creation(self):
        notification = Notification.objects.create(
            user=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        self.assertEqual(notification.is_read, False)
        self.assertEqual(notification.user, self.user)


class SearchTest(TestCase):
    """Tests para búsqueda"""
    
    def setUp(self):
        self.client = Client()
        self.developer = Developer.objects.create(name='Search Dev')
        self.game1 = Game.objects.create(
            title='Action Game',
            description='An action game',
            release_date='2024-01-01',
            price=29.99,
            developer=self.developer
        )
        self.game2 = Game.objects.create(
            title='RPG Game',
            description='A role playing game',
            release_date='2024-01-01',
            price=39.99,
            developer=self.developer
        )
    
    def test_search_by_title(self):
        response = self.client.get(reverse('library:game_list'), {'q': 'Action'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Action Game')
        self.assertNotContains(response, 'RPG Game')
    
    def test_search_by_description(self):
        response = self.client.get(reverse('library:game_list'), {'q': 'role playing'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RPG Game')

