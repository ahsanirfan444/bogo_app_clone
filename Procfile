web: gunicorn --bind :8000 --workers 3 --threads 2 sockets.wsgi:application
websocket: daphne -b :: -p 5000 sockets.asgi:application