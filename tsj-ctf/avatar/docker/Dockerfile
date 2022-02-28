FROM php:8-apache

RUN pecl install redis && docker-php-ext-enable redis
RUN apt update && apt install -y libzip-dev && docker-php-ext-install pdo pdo_mysql zip

COPY ./src/ /var/www/

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN cd /var/www/ && composer install

RUN chmod 1733 /tmp

COPY ./flag/readflag.c /readflag.c
COPY ./flag/flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag
