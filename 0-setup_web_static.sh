#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
if ! command -v nginx > /dev/null 2>&1; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create the folder /data/ if it doesn’t already exist
if [ ! -d "/data/" ]; then
    sudo mkdir /data/
fi

# Create the folder /data/web_static/ if it doesn’t already exist
if [ ! -d "/data/web_static/" ]; then
    sudo mkdir /data/web_static/
fi

# Create the folder /data/web_static/releases/ if it doesn’t already exist
if [ ! -d "/data/web_static/shared" ]; then
    sudo mkdir /data/web_static/releases/
fi

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
if [ ! -d "/data/web_static/releases/test/" ]; then
    sudo mkdir /data/web_static/releases/test/
fi

# Create a fake HTML file /data/web_static/releases/test/index.html
if [ ! -f "/data/web_static/releases/test/index.html" ]; then
    sudo touch /data/web_static/releases/test/index.html
fi

# Write a fake HTML content
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
if [ -L "/data/web_static/current" ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

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
    index index.html index.htm index.nginx-debian.html;
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
