FROM php:8-apache

# enable Apache rewrite module
RUN a2enmod rewrite

# Install php extensions
RUN apt update && apt install -y libzip-dev && docker-php-ext-install zip

# initialize the web application
COPY ./src/ /var/www/
RUN chmod 1733 /var/www/html/uploads
RUN chmod 1733 /tmp

# install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN cd /var/www/ && composer install

# Set up flag & readflag for CTF
COPY ./flag/readflag.c /readflag.c
COPY ./flag/flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag
