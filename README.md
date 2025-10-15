Project: Энциклопедия Разработки Игр

Коротко:
- Django проект с приложениями `games` и `users`.
- Локальный запуск: создайте виртуальное окружение, установите зависимости и выполните миграции.

Local quickstart
----------------
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # опционально
python manage.py runserver 0.0.0.0:8000
```

Deployment checklist (summary)
------------------------------
1. Подготовьте сервер (Ubuntu/Debian): установите Python 3.11+, git, nginx, certbot.
2. Клонируйте проект в `/var/www/mylibrary` и создайте виртуальное окружение в папке `venv`.
3. Скопируйте `.env.example` в `/var/www/mylibrary/.env` и заполните реальные значения (`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, и т.д.).
4. Установите зависимости: `venv/bin/pip install -r requirements.txt`.
5. Выполните миграции и соберите статику:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
6. Настройте systemd unit (файл `deploy/gunicorn-mylibrary.service`) и включите его:
   ```bash
   sudo cp deploy/gunicorn-mylibrary.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now gunicorn-mylibrary
   ```
7. Настройте Nginx: скопируйте `deploy/nginx_mylibrary.conf` в `/etc/nginx/sites-available/mylibrary` и создайте ссылку в `sites-enabled`.
8. SSL: используйте certbot `sudo certbot --nginx -d mylibrary.kz -d www.mylibrary.kz`.

Статика и медиа (пункт 7 рубрики)
--------------------------------
- Статика: `STATIC_ROOT` в `settings.py` указывает на `staticfiles`. На сервере выполните `collectstatic` и настройте Nginx отдавать `/static/` из этой директории (пример конфигурации в `deploy/nginx_mylibrary.conf`). WhiteNoise уже включён и полезен, но при использовании Nginx рекомендуем отдавать статику напрямую.
- Медиа (загрузки пользователей): `MEDIA_ROOT` в `settings.py` указывает на `media`. В продакшне Nginx должен отдавать `/media/` напрямую (в данном конфиге это настроено). Альтернатива: хранить медиа на S3 и использовать `django-storages`.

Domain
------
Ensure storage directories
-------------------------
Before running the site in production, create the storage directories and set permissions. You can run the included management command which creates `STATIC_ROOT` and `MEDIA_ROOT` (uses paths from `settings.py`):

```powershell
# activate your venv first
python manage.py ensure_storage
```

Or manually on the server:

```bash
mkdir -p /var/www/mylibrary/staticfiles
mkdir -p /var/www/mylibrary/media
chown -R www-data:www-data /var/www/mylibrary
chmod -R 755 /var/www/mylibrary/staticfiles /var/www/mylibrary/media
```

After directories are created run:

```bash
python manage.py collectstatic --noinput
```

- После настройки и проверки, добавьте ваш домен `mylibrary.kz` в `DJANGO_ALLOWED_HOSTS` в `.env`.
- Не храните `DEBUG=True` в продакшне.

Если хотите, могу автоматически:
- вернуть и обновить `README.md` из `archive_removed/`,
- сгенерировать пример `nginx` и `systemd` (уже добавлены в `deploy/`),
- помочь подготовить `.env` и инструкции конкретно под выбранный хостинг.
