#!/usr/bin/env python3

import subprocess
import os
import sys

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def main():
    if os.geteuid() != 0:
        print("Run as root")
        sys.exit(1)

    run("apt-get update -y")
    run("apt-get upgrade -y")

    run("apt-get install -y nginx mariadb-server php-fpm php-mysql unzip curl wget")

    run("systemctl enable nginx")
    run("systemctl start nginx")

    run("systemctl enable mariadb")
    run("systemctl start mariadb")

    run("mysql -e \"CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;\"")
    run("mysql -e \"CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'wppassword';\"")
    run("mysql -e \"GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';\"")
    run("mysql -e \"FLUSH PRIVILEGES;\"")

    os.chdir("/tmp")
    run("wget https://wordpress.org/latest.zip")
    run("unzip latest.zip")

    run("mv wordpress /var/www/html/wordpress")
    run("chown -R www-data:www-data /var/www/html/wordpress")
    run("chmod -R 755 /var/www/html/wordpress")

    nginx_config = """
server {
    listen 80;
    server_name localhost;

    root /var/www/html/wordpress;
    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php-fpm.sock;
    }
}
"""

    with open("/etc/nginx/sites-available/wordpress", "w") as f:
        f.write(nginx_config)

    run("ln -sf /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/")
    run("rm -f /etc/nginx/sites-enabled/default")

    run("systemctl restart nginx")
    run("systemctl restart php*-fpm")

    print("WordPress LEMP setup completed.")

if __name__ == "__main__":
    main()