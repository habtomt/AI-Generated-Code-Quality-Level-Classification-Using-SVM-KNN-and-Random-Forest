"""
Auto-generated Python code
Scenario : Web Hosting & Deployment
Prompt   : response_002.txt
Run      : 2
"""

bash
#!/bin/bash

# Update package list
sudo apt update

# Install Apache2
sudo apt install apache2 -y

# Install MySQL
sudo apt install mysql-server mysql-client -y

# Install PHP8.1
sudo apt install php8.1 libapache2-mod-php8.1 php8.1-mysql php8.1-curl php8.1-gd php8.1-mbstring php8.1-intl php8.1-xml php8.1-zip -y

# Install MariaDB (alternative to MySQL)
sudo apt install mariadb-server mariadb-client -y

# Configure MariaDB
echo "Updating MariaDB root password..."
sudo mysqladmin -u root password YOUR_MYSQL_ROOT_PASSWORD

echo "Creating a new MariaDB database for WordPress..."
sudo mysql -u root -pYOUR_MYSQL_ROOT_PASSWORD -e "CREATE DATABASE wordpress;"

echo "Creating a new MariaDB user for WordPress..."
sudo mysql -u root -pYOUR_MYSQL_ROOT_PASSWORD -e "CREATE USER 'wordpressuser'@'localhost' IDENTIFIED BY 'YOUR_MYSQL_USER_PASSWORD';"

echo "Granting permissions to the new user..."
sudo mysql -u root -pYOUR_MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpressuser'@'localhost';"

echo "Flushing privileges..."
sudo mysql -u root -pYOUR_MYSQL_ROOT_PASSWORD -e "FLUSH PRIVILEGES;"

# Configure Apache2
echo "Enabling Apache2 rewrite module..."
sudo a2enmod rewrite -y

echo "Creating a new Apache2 virtual host for WordPress..."
sudo tee /etc/apache2/sites-available/wordpress.conf <<EOF
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName example.com
    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

echo "Enabling the new virtual host..."
sudo a2ensite wordpress.conf -y

echo "Restarting Apache2..."
sudo service apache2 restart

# Create a new WordPress directory
echo "Creating a new WordPress directory..."
sudo mkdir /var/www/html

# Download WordPress
echo "Downloading WordPress..."
wget https://wordpress.org/latest.tar.gz -O /var/www/html/wordpress.tar.gz

echo "Extracting WordPress..."
cd /var/www/html
tar -xvzf wordpress.tar.gz
rm wordpress.tar.gz

# Change permissions
echo "Changing permissions..."
sudo chown -R www-data:www-data /var/www/html

# Configure WordPress
echo "Configuring WordPress..."
sudo tee /var/www/html/wp-config.php <<EOF
<?php
define('DB_NAME', 'wordpress');
define('DB_USER', 'wordpressuser');
define('DB_PASSWORD', 'YOUR_MYSQL_USER_PASSWORD');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');
\$table_prefix = 'wp_';
define('AUTH_KEY', 'YOUR_WPCOM_AUTH_KEY');
define('SECURE_AUTH_KEY', 'YOUR_WPCOM_SECURE_AUTH_KEY');
define('LOGGED_IN_KEY', 'YOUR_WPCOM_LOGGED_IN_KEY');
define('NONCE_KEY', 'YOUR_WPCOM_NONCE_KEY');
define('AUTH_SALT', 'YOUR_WPCOM_AUTH_SALT');
define('SECURE_AUTH_SALT', 'YOUR_WPCOM_SECURE_AUTH_SALT');
define('LOGGED_IN_SALT', 'YOUR_WPCOM_LOGGED_IN_SALT');
define('NONCE_SALT', 'YOUR_WPCOM_NONCE_SALT');
EOF

echo "Setting up WordPress..."
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html

echo "Restarting Apache2..."
sudo service apache2 restart