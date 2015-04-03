# python-flask27

Installation
------------

```bash
mkdir -p /var/www/flask
git clone "https://github.com/mykysyk/python-flask27.git" /var/www/flask
cd /var/www/flask
python -c "from app_sample.database import init_db;init_db()"
chown nginx:nginx -R /var/www/flask
```


