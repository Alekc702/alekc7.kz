#!/usr/bin/env bash
set -e

# Minimal VPS deploy script for Ubuntu (run on the VPS as a sudo-capable user)
# Replace <REPO_URL> with your git repository URL and set environment variables as instructed below.

# 1) Install system packages
sudo apt update
sudo apt install -y python3-pip python3-venv git nginx

# 2) Prepare project directory
sudo mkdir -p /var/www/mylibrary
sudo chown $USER:$USER /var/www/mylibrary
if [ ! -d "/var/www/mylibrary/.git" ]; then
  git clone <REPO_URL> /var/www/mylibrary
else
  cd /var/www/mylibrary && git pull
fi

cd /var/www/mylibrary

# 3) Create virtualenv and install requirements
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4) Environment variables (set these appropriately, e.g. in a systemd unit or env file)
# Example:
# export DJANGO_SECRET_KEY='your-secret-key'
# export DJANGO_DEBUG='False'
# export DJANGO_ALLOWED_HOSTS='mylibrary.kz,www.mylibrary.kz'
# export DATABASE_URL='postgres://USER:PASS@HOST:PORT/NAME'

# 5) Django maintenance
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 6) Install systemd service (requires sudo)
sudo cp deploy/gunicorn-mylibrary.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-mylibrary

# 7) Nginx configuration
sudo cp deploy/nginx_mylibrary.conf /etc/nginx/sites-available/mylibrary
sudo ln -sf /etc/nginx/sites-available/mylibrary /etc/nginx/sites-enabled/mylibrary
sudo nginx -t
sudo systemctl restart nginx

# 8) Obtain TLS certificate via Certbot (interactive)
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d mylibrary.kz -d www.mylibrary.kz

# Notes:
# - Ensure `gunicorn-mylibrary.service` has correct WorkingDirectory and PATH for your venv.
# - Consider storing sensitive env vars in /etc/environment or a systemd EnvironmentFile and reference it in the unit file.
# - After changing code: git pull, activate venv, pip install -r requirements.txt (if needed), python manage.py migrate, python manage.py collectstatic, sudo systemctl restart gunicorn-mylibrary

