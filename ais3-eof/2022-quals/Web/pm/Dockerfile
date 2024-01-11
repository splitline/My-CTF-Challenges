FROM php:7.0-fpm

RUN apt-get update -y && apt-get install -y nginx

RUN echo 'disable_functions = "shell_exec, system"' >> /usr/local/etc/php/conf.d/docker-php.ini;
RUN echo 'max_execution_time = 3' >> /usr/local/etc/php/conf.d/docker-php.ini;
RUN echo "request_terminate_timeout = 3" >> /usr/local/etc/php-fpm.d/www.conf;

COPY nginx-site.conf /etc/nginx/sites-enabled/default
COPY entrypoint.sh /etc/entrypoint.sh
RUN chmod +x /etc/entrypoint.sh

COPY ./src /var/www/html
RUN chmod -R 755 /var/www/html
RUN chown root:root /var/www/html

WORKDIR /var/www/html

# Set up flag & readflag for CTF
COPY ./flag/readflag.c /readflag.c
COPY ./flag/flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag

EXPOSE 80
ENTRYPOINT ["/etc/entrypoint.sh"]