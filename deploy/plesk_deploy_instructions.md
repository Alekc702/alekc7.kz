Plesk: подробная инструкция по развертыванию Django-проекта

1) Предпосылки
- У вас есть репозиторий на GitHub (HTTPS URL).
- В Plesk вы имеете доступ к разделу "Git" (как на скриншотах).

2) Клонирование репозитория в Plesk
- В Plesk -> Sites & Domains -> ваш домен -> Git -> Add Repository
- Выберите "Remote repository"
- URL: вставьте HTTPS URL вашего репозитория
- Repository name: al ekc7.git (или любое)
- Deployment mode: Automatic
- Server path: /httpdocs  (или /httpdocs/mylibrary если хотите подпапку)
- Включите "Additional deployment actions"

3) Команда дополнительных действий (копировать как одну строку)
/bin/bash -lc "cd /var/www/vhosts/alekc7.kz/httpdocs && python3 -m venv venv || true && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput"

4) Что делать если команда не выполняется
- Если в логах вы увидите `python: command not found` или `pip: command not found` — значит на сервере нет доступного python3/pip в shell окружении. В этом случае:
  - Проверьте в Plesk, есть ли пункт "Python" (Python application). Если да, используйте его: укажите path, WSGI script (mylibrary/wsgi.py) и попросите Plesk установить requirements.txt через UI.
  - Если "Python" нет, откройте тикет в техподдержку с просьбой включить Python/WSGI или дать SSH доступ.

5) Создание базы данных
- В Plesk -> Databases -> Add Database
- Выберите MySQL (или MariaDB), создайте имя БД и пользователя. Запомните параметры для Django.

6) Настройка WSGI (если доступно)
- В Plesk -> Python -> Create application
- Application root: путь где развернут проект (/httpdocs или подпапка)
- WSGI entry point: mylibrary/wsgi.py
- Create virtual environment: yes
- Install requirements: указать requirements.txt (Plesk может предложить поле)
- Запустите приложение

7) SSL
- Plesk -> SSL/TLS Certificates -> Let's Encrypt (если доступно) или используйте hoster.kz/ssl

8) Если нужно — обращение в поддержку (готовое сообщение)
```
Здравствуйте, у меня домен alekc7.kz (аккаунт alekc7_kz). Я развернул код Django через Git, но не могу выполнить установки зависимостей или выполнить manage.py команды через Plesk. Прошу включить поддержку Python 3.x и WSGI (Phusion Passenger) для домена или предоставить SSH доступ для пользователя alekc7_kz.
Спасибо.
```
