import subprocess
import os

def setup_lemp_stack():
    """
    Automates the installation and configuration of a LEMP stack
    (Linux, Nginx, MariaDB, PHP) for WordPress.
    """
    
    # Update and install system dependencies
    commands = [
        ["sudo", "apt", "update"],
        ["sudo", "apt", "install", "-y", "nginx", "mariadb-server", "php-fpm", "php-mysql", "php-curl", "php-gd", "php-intl", "php-mbstring", "php-soap", "php-xml", "php-xmlrpc", "php-zip"]
    ]

    for cmd in commands:
        subprocess.run(cmd, check=True)

    # Database Configuration
    db_setup = """
    CREATE DATABASE wordpress_db;
    CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'secure_password';
    GRANT ALL PRIVILEGES ON wordpress_db.* TO 'wp_user'@'localhost';
    FLUSH PRIVILEGES;
    """
    subprocess.run(["sudo", "mysql", "-e", db_setup], check=True)

    # WordPress Installation
    subprocess.run(["wget", "-P", "/tmp", "https://wordpress.org/latest.tar.gz"], check=True)
    subprocess.run(["tar", "-xzvf", "/tmp/latest.tar.gz", "-C", "/tmp"], check=True)
    subprocess.run(["sudo", "cp", "-a", "/tmp/wordpress/.", "/var/www/html/wordpress"], check=True)
    
    # Set Permissions for Updates and Plugins
    subprocess.run(["sudo", "chown", "-R", "www-data:www-data", "/var/www/html/wordpress"], check=True)
    subprocess.run(["sudo", "find", "/var/www/html/wordpress", "-type", "d", "-exec", "chmod", "755", "{}", ";"], check=True)
    subprocess.run(["sudo", "find", "/var/www/html/wordpress", "-type", "f", "-exec", "chmod", "644", "{}", ";"], check=True)

    # Nginx Configuration
    nginx_config = """
server {
    listen 80;
    server_name localhost;
    root /var/www/html/wordpress;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires max;
        log_not_found off;
    }
}
"""
    config_path = "/etc/nginx/sites-available/wordpress"
    with open("wordpress_nginx", "w") as f:
        f.write(nginx_config)
    
    subprocess.run(["sudo", "mv", "wordpress_nginx", config_path], check=True)
    subprocess.run(["sudo", "ln", "-s", config_path, "/etc/nginx/sites-enabled/"], check=True)
    subprocess.run(["sudo", "rm", "/etc/nginx/sites-enabled/default"], check=False)
    
    # Restart Services
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    subprocess.run(["sudo", "systemctl", "restart", "php8.1-fpm"], check=True)

if __name__ == "__main__":
    setup_lemp_stack()