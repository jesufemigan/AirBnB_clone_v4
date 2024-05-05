#!/usr/bin/env bash
#sets up server for deployment of web_static

#install nginx if it is not installed
function install() {
	if ! command -v "$1" &> /dev/null; then
		echo -e "\t Installing nginx...\n"
		sudo apt-get update -y -qq
		sudo apt-get install -y -qq "$1"
		echo -e "\nSuccessfully installed nginx\n"
		echo -e "\nSetting up Nginx..."
		sudo ufw allow 'Nginx HTTP'
		echo -e "Nginx is set up successfully!...\n"
	else
		echo -e "\nNginx is already installed.\n"
	fi
}
install nginx

#web_static_dir="/data/web_static/"
#shared="/shared/"
#releases="/releases/test/"

#if [ ! -d "$web_static_dir" ]; then
	#mkdir -p "$web_static_dir"

	#if [ ! -d "$web_static_dir""$shared" ]; then
		#mkdir "$web_static_dir""$shared"
	#fi
	#if [ ! -d "$web_static_dir""$releases" ]; then
		#mkdir -p "$web_static_dir""$releases" 
	#fi
#fi
sudo mkdir -p /data/web_static/{releases/test,shared}

fake_html="<html><head></head><body>Holberton School</body></html>"
echo "$fake_html" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current
#sym_link="/data/web_static/current/"

#if [ -L "$sym_link" ]; then
#	rm -f "$sym_link"
#	ln -s "$web_static_dir""$releases" "$sym_link"
#else
#	ln -s "$web_static_dir""$releases" "$sym_link"
#fi

sudo chown -R ubuntu:ubuntu /data/

#new_block='\
#	location /hbnb_static {\
#		alias /data/web_static/current/;\
#	}'
nginx_config="/etc/nginx/sites-available/default"

if [ -f "$nginx_config" ]; then
	if grep -q "location /hbnb_static" "$nginx_config"; then
		echo "Configuration block for hbnb_static exists in $nginx_config"
	else
		sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' "$nginx_config"
		echo "Added configuration block for hbnb_static"
	fi
else
	echo "NGINX not properly configured as $nginx_config does not exist"
fi
sudo service nginx restart
echo -e "\nWeb Server set up successfully for deployment."
