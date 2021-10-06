# Server Configuration

This is the document how I start **Nginx** + **Gunicorn** + **Sanic** server   
The reason why I use Sanic is to make request async   

## Install Python Components
---

Install default components used for python building   

```
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

## Creating a Python Virtual Environment
---

Install `python3-venv`   

```
sudo apt install python3-venv
```

Create virtual environment   

```
python3 -m venv venv
source venv/bin/activate
```

Install **Sanic** and **Gunicorn**   

```
pip3 install wheel
pip3 install gunicorn sanic
```

Also, you should install **konlpy** and **mecab**   

```
pip3 install konlpy
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)

cd /tmp
cd mecab-python-0.996
python3 setup.py build
python3 setup.py install
```

Check `app.py` is running   

```
python3 app.py
```

Visit your IP address followed by `:5000` in your web browser   

## Configure Gunicorn
---

Bind your app to gunicorn

```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Visit again your IP address followed by `:5000` in your web browser   

Deactivate your virtual environment by `deactivate`   

Create a service file   

```
sudo vi /etc/systemd/system/app.service
```

```
[Unit]
Description=Gunicorn instance to serve app
After=network.target

[Service]
User=[username]
Group=www-data
WorkingDirectory=[server directory]
Environment="PATH=[server directory]:/bin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin"
ExecStart=[server directory]/venv/bin/gunicorn --workers 5 --threads 4 --worker-class sanic.worker.GunicornWorker --bind unix:[server directory]/app.sock -m 007 -t 60 wsgi:app

[Install]
WantedBy=multi-user.target
```

Start service   

```
sudo systemctl start app
sudo systemctl enable app
```

Check service is running properly

```
sudo systemctl status app
```

## Configure Nginx
---

Install Nginx   

```
sudo apt install nginx
```

Configure Gunicorn server

```
sudo nano /etc/nginx/sites-available/app
```

```
server {
    listen 80;
    server_name [your domain];

    location / {
        include proxy_params;
        proxy_pass http://unix:[server directory]/app.sock;
    }
}
```

Make symbolic link to `sites-enabled`   

```
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
```

Check if error is contained   

```
sudo nginx -t
```

Restart Nginx process   

```
sudo systemctl restart nginx
```

Visit your IP address in your web browser   

