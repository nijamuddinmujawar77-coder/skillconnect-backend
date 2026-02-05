import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser

# Create superuser if not exists
email = 'nijamuddinmujawar77@gmail.com'
password = 'admin123'

if not CustomUser.objects.filter(email=email).exists():
    user = CustomUser.objects.create_superuser(
        email=email,
        password=password,
        first_name='Nijamuddin',
        last_name='Mujawar'
    )
    print(f'✅ Superuser created: {email}')
else:
    print(f'⏭️ Superuser already exists: {email}')
