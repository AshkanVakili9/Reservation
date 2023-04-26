
# Generate new secret key

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"


py -m venv venv

venv\scripts\activate

cd backend

pip install -r req.txt

python manage.py generate_city
