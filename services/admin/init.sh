#!/bin/bash
# Initialize Admin service Django app

echo "Running Django migrations..."
python manage.py migrate --run-syncdb

echo "Creating superuser..."
python manage.py shell <<END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@swap.local',
        password='AdminSwap123!'
    )
    print("Superuser 'admin' created successfully!")
else:
    print("Superuser 'admin' already exists!")
END

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Admin service initialized!"
