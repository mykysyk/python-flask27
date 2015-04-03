# python-flask27

Installation
------------

```bash
mkdir -p /var/www/flask
git clone "https://github.com/mykysyk/python-flask27.git" /var/www/flask
cd /var/www/flask
python -c "from app_sample.database import init_db;init_db()"
chown nginx:nginx -R /var/www/flask
pip install Flask Jinja2 SQLAlchemy uWSGI
```

```bash
vi /etc/nginx/uwsgi.ini
```
>
```ini
#http://uwsgi-docs.readthedocs.org/en/latest/Systemd.html
[uwsgi]
socket      = /var/lib/nginx/tmp/uwsgi/uwsgi.sock
python-path = /var/www/flask
wsgi-file   = /var/www/flask/index.wsgi
uid         = nginx
gid         = nginx
processes   = 1
threads     = 10
stats       = 127.0.0.1:9191
```

```bash
vi /etc/systemd/system/uwsgi.service
```
>
```ini
[Unit]
Description=uWSGI
After=syslog.target
>
[Service]
ExecStart=/bin/uwsgi --ini /etc/nginx/uwsgi.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all
>
[Install]
WantedBy=multi-user.target
```

```bash
systemctl start  uwsgi.service
systemctl status uwsgi.service
```

```bash
vi /etc/nginx/nginx.conf
```
>
```conf
user  nginx;
worker_processes  1;
error_log  /var/log/nginx/error.log;
pid        /run/nginx.pid;
events {
    worker_connections  1024;
}
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    access_log  /var/log/nginx/access.log  main;
    sendfile        on;
    keepalive_timeout  65;
    index   index.html index.htm;
    include /etc/nginx/conf.d/*.conf;
    server {
        listen       80 default_server;
        server_name  localhost;
        root         /usr/share/nginx/html;
        include /etc/nginx/default.d/*.conf;
        location / {
                include uwsgi_params;
                uwsgi_pass unix:/var/lib/nginx/tmp/uwsgi/uwsgi.sock;
        }
        error_page  404              /404.html;
        location = /40x.html {
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
        }
    }
}
```

```bash
systemctl restart nginx.service
systemctl status  nginx.service
```
