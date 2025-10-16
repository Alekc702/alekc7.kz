# Энциклопедия разработки игр (alekc7.kz)

Проект на Django: каталог игр с CRUD, авторизацией, загрузкой обложек и JSON API. Развёрнут на Render.

- Продакшн: https://alekc7.kz
- Резерв: https://alekc7-kz.onrender.com
- Репозиторий: https://github.com/Alekc702/alekc7.kz

## Локальный запуск

```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py ensure_storage
python manage.py createsuperuser  # опционально
python manage.py runserver 0.0.0.0:8000
```

## Что внутри
- Приложения: `games`, `users`
- Шаблоны: наследование от `templates/base.html`, страницы списка/детали/форм
- Статика: `static/` (CSS/JS/изображения), WhiteNoise
- Медиа: `MEDIA_ROOT` (локально `media/`, в проде `/var/data/media`), загрузка обложек в `game_covers/`
- Админка: зарегистрированы модели с фильтрами
- API: `/api/games/`, `/api/games/<id>/` (требуется API-ключ)

### Доступ к API по ключу
- Включается переменной окружения `DJANGO_API_KEY` (см. `settings.py`). Если ключ не задан, API возвращает 401.
- Клиент передаёт ключ либо в заголовке `X-API-Key: <ключ>`, либо как параметр `?api_key=<ключ>`.

Примеры (PowerShell):

```powershell
# Запуск локально с ключом в этой сессии
$env:DJANGO_API_KEY = 'ваш-длинный-случайный-ключ'
python manage.py runserver

# Запросы с ключом в заголовке
curl http://localhost:8000/api/games/ -H "X-API-Key: ваш-длинный-случайный-ключ"
curl http://localhost:8000/api/games/1/ -H "X-API-Key: ваш-длинный-случайный-ключ"

# Или в query-параметре
curl "http://localhost:8000/api/games/?api_key=ваш-длинный-случайный-ключ"
curl "http://localhost:8000/api/games/1/?api_key=ваш-длинный-случайный-ключ"
```

## Продакшн (Render)
Конфигурация в `render.yaml` и `Procfile`.

Основные переменные окружения:
- `DJANGO_SECRET_KEY` — секретный ключ
- `DJANGO_DEBUG=False` — продакшн режим
- `DJANGO_ALLOWED_HOSTS` — домены (через запятую): `alekc7-kz.onrender.com,alekc7.kz,www.alekc7.kz`
- `DJANGO_CSRF_TRUSTED_ORIGINS` — `https://alekc7-kz.onrender.com,https://alekc7.kz,https://www.alekc7.kz`
- `DJANGO_MEDIA_ROOT=/var/data/media` — путь для медиа на подключённом диске
- `DJANGO_API_KEY` — ключ доступа к JSON API

Хранилище медиа: используется Disk (план Starter) с монтированием в `/var/data`.

## Домены
1) Добавьте домен в Render (Custom Domains) и укажите DNS:
   - `www`: CNAME → `alekc7-kz.onrender.com`
   - apex (`@`): ALIAS/ANAME → `alekc7-kz.onrender.com` (или A-запись по документации провайдера)
2) Обновите окружение сервиса (см. переменные выше).

## Инициализация данных
Есть фикстура `fixtures/games_initial_data.json` и команда:

```powershell
python manage.py ensure_seed
```

Загружает стартовые данные, если база пуста.

## Примечания
- Секреты в репозиторий не коммитим
- Статика собирается командой `collectstatic`
- Для долгосрочного хранения медиа можно переключиться на S3 (см. `settings.py`)
- Не храните `DEBUG=True` в продакшне
