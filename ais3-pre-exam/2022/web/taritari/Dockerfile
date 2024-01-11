FROM php:8-apache

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

COPY src/ /var/www/html/
RUN chmod -R 755 /var/www/html
RUN chown root:root /var/www/html

RUN mkdir -p /var/www/html/files/
RUN chown www-data:www-data /var/www/html/files/
RUN chmod 1733 /var/www/html/files/

RUN echo "AIS3{test_flag (to be changed)}" > /y000000_i_am_the_f14GGG.txt
