FROM php:7.4-apache

RUN apt update
RUN apt install netcat-openbsd -qy
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
