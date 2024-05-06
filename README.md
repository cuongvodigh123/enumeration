# enumeration
cài đặt apache2
lưu thư mục www như trên
cấu hình
trong file etc/apache2.conf
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride None
	Require all granted
</Directory>

trong file /etc/sites-available/000-default.conf
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    
    ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
    <Directory "/var/www/cgi-bin/">
        Options +ExecCGI
        AddHandler cgi-script .cgi
        Require all granted
    </Directory>
</VirtualHost>

trong file /etc/sites-enabled/000-default.conf
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    
    ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
    <Directory "/var/www/cgi-bin/">
        Options +ExecCGI
        AddHandler cgi-script .cgi
        Require all granted
    </Directory>
</VirtualHost>

trong file /etc/sudoers thêm 2 dòng sau

www-data ALL=(ALL) NOPASSWD: /usr/bin/*
www-data ALL=(ALL) NOPASSWD: /usr/sbin/*

chmod +x /var/www/cgi-bin/*
sudo a2enmod cgi
sudo service apache2 restart