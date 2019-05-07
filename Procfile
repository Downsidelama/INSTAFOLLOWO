release: python manage.py migrate ; python manage.py collectstatic
web: gunicorn instafollowo.wsgi --log-file -
