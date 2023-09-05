 #!/usr/bin/env bash

set -o errexit  # exit when there is an error error
pip install --upgrade pip
pip install -r requirements.txt

# python manage.py collectstatic --no-input
python manage.py migrate

if [[ $CREATE_SUPERUSER ]]; then
  export DJANGO_SUPERUSER_EMAIL=admin@gmail.com
  export DJANGO_SUPERUSER_PASSWORD=2000money
  export DJANGO_SUPERUSER_FIRST_NAME=Admin1
  export DJANGO_SUPERUSER_LAST_NAME=Admin2

  python manage.py createsuperuser --noinput
fi

