set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [ "$CREATE_SUPERUSER" = "true" ]; then
    # Createsuperuser with --no-input requires DJANGO_SUPERUSER_USERNAME,
    # DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD env vars
    python manage.py createsuperuser --no-input || true
fi
