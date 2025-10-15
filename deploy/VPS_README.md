VPS Deployment Notes

DNS
- At your domain registrar create A records:
  - @ -> <VPS_IP>
  - www -> <VPS_IP>
- Wait for DNS propagation (can take minutes to hours).

Systemd
- Service file is `deploy/gunicorn-mylibrary.service`. Copy it to `/etc/systemd/system/` and run `sudo systemctl daemon-reload`.
- Ensure the service runs as `www-data` (or change User/Group to your deploy user).

Nginx
- `deploy/nginx_mylibrary.conf` is a template. Copy to `/etc/nginx/sites-available/mylibrary` and symlink to sites-enabled.
- Paths in the config should point to where you collected static files (default in settings is `staticfiles` inside project root).

TLS
- Use Certbot for Let's Encrypt:
  - `sudo apt install certbot python3-certbot-nginx`
  - `sudo certbot --nginx -d mylibrary.kz -d www.mylibrary.kz`

Environment Variables
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=mylibrary.kz,www.mylibrary.kz`.
- If using Postgres, set `DATABASE_URL`.

Rollback / Updates
- To update: git pull, activate venv, pip install -r requirements.txt, python manage.py migrate, python manage.py collectstatic --noinput, sudo systemctl restart gunicorn-mylibrary

