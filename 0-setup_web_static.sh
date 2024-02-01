#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
if ! command -v nginx > /dev/null 2>&1; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
if [ ! -f "/etc/nginx/sites-available/default" ]; then
    sudo touch /etc/nginx/sites-available/default
fi

# Write the following configuration:
echo "server {
    listen 80;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 https://www.alemiherbert.github.io/;
    }
    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}" | sudo tee /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart
