FROM python:3.8.5

RUN apt-get update
RUN apt-get install xinetd -qy
RUN useradd -m cat_translator
COPY ./share /home/cat_translator
COPY ./xinetd /etc/xinetd.d/cat_translator
COPY ./flag /flag_aeab2c0bd54414b481a0b7683119ac8d
RUN chown -R root:root /home/cat_translator
RUN chmod -R 755 /home/cat_translator

CMD ["/usr/sbin/xinetd","-dontfork"]
