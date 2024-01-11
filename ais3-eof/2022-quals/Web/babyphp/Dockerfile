FROM php:7.4-apache

COPY src/ /var/www/html/

RUN chmod -R 755 /var/www/html
RUN chown root:root /var/www/html

RUN chown www-data:www-data /var/www/html/sandbox/
RUN chmod +w /var/www/html/sandbox/
RUN touch /var/www/html/sandbox/.htaccess
RUN touch /var/www/html/sandbox/index.php

RUN echo 'FLAG{Pecchipee://filter/k!ng}' > /za_f14g.txt