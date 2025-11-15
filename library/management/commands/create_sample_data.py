"""
Management command para crear datos de ejemplo
"""
from django.core.management.base import BaseCommand
from library.models import User, Developer, Category, Game, UserLibrary, Review
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el sistema'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de ejemplo...')

        # Crear usuarios
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'is_premium': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f'Usuario admin creado: {admin_user.username}'))

        user1, _ = User.objects.get_or_create(
            username='usuario1',
            defaults={
                'email': 'usuario1@example.com',
                'bio': 'Gamer apasionado'
            }
        )
        user1.set_password('usuario123')
        user1.save()
        self.stdout.write(self.style.SUCCESS(f'Usuario creado: {user1.username}'))

        # Crear desarrolladores
        dev1, _ = Developer.objects.get_or_create(
            name='Valve Corporation',
            defaults={'country': 'USA', 'description': 'Desarrollador de Steam'}
        )
        dev2, _ = Developer.objects.get_or_create(
            name='CD Projekt RED',
            defaults={'country': 'Poland', 'description': 'Desarrollador de The Witcher'}
        )
        dev3, _ = Developer.objects.get_or_create(
            name='Rockstar Games',
            defaults={'country': 'USA', 'description': 'Desarrollador de GTA'}
        )
        self.stdout.write(self.style.SUCCESS('Desarrolladores creados'))

        # Crear categorías
        cat1, _ = Category.objects.get_or_create(name='Acción')
        cat2, _ = Category.objects.get_or_create(name='RPG')
        cat3, _ = Category.objects.get_or_create(name='Aventura')
        cat4, _ = Category.objects.get_or_create(name='Estrategia')
        self.stdout.write(self.style.SUCCESS('Categorías creadas'))

        # Crear juegos
        games_data = [
            {
                'title': 'Half-Life 2',
                'description': 'Un juego de acción y aventura épico',
                'release_date': date(2004, 11, 16),
                'price': Decimal('9.99'),
                'developer': dev1,
                'categories': [cat1, cat3]
            },
            {
                'title': 'The Witcher 3: Wild Hunt',
                'description': 'RPG de mundo abierto con una historia épica',
                'release_date': date(2015, 5, 19),
                'price': Decimal('39.99'),
                'developer': dev2,
                'categories': [cat2, cat3]
            },
            {
                'title': 'Grand Theft Auto V',
                'description': 'Aventura de mundo abierto en Los Santos',
                'release_date': date(2013, 9, 17),
                'price': Decimal('29.99'),
                'developer': dev3,
                'categories': [cat1, cat3]
            },
            {
                'title': 'Portal 2',
                'description': 'Puzzle y plataformas con portales',
                'release_date': date(2011, 4, 19),
                'price': Decimal('9.99'),
                'developer': dev1,
                'categories': [cat1, cat3]
            },
            {
                'title': 'Cyberpunk 2077',
                'description': 'RPG de ciencia ficción en Night City',
                'release_date': date(2020, 12, 10),
                'price': Decimal('59.99'),
                'developer': dev2,
                'categories': [cat2, cat1]
            },
        ]

        for game_data in games_data:
            categories = game_data.pop('categories')
            game, created = Game.objects.get_or_create(
                title=game_data['title'],
                defaults=game_data
            )
            game.categories.set(categories)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Juego creado: {game.title}'))

        # Agregar juegos a biblioteca de usuario1
        games = Game.objects.all()[:3]
        for game in games:
            library_item, created = UserLibrary.objects.get_or_create(
                user=user1,
                game=game,
                defaults={
                    'hours_played': Decimal('25.5'),
                    'is_favorite': game.title == 'The Witcher 3: Wild Hunt'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Juego agregado a biblioteca: {game.title}'))

        # Crear reseñas
        witcher = Game.objects.get(title='The Witcher 3: Wild Hunt')
        Review.objects.get_or_create(
            user=user1,
            game=witcher,
            defaults={
                'rating': 5,
                'comment': 'Excelente juego, historia increíble y mundo abierto impresionante.'
            }
        )

        self.stdout.write(self.style.SUCCESS('\n¡Datos de ejemplo creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('\nUsuarios de prueba:'))
        self.stdout.write(self.style.SUCCESS('  - admin / admin123 (staff)'))
        self.stdout.write(self.style.SUCCESS('  - usuario1 / usuario123'))

