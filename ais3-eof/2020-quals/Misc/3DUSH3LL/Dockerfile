FROM python:3.8.5

RUN apt-get update
RUN apt-get install xinetd -qy
RUN useradd -m pyshell
COPY ./share /home/pyshell
COPY ./xinetd /etc/xinetd.d/pyshell
COPY ./flag /flag_d053472057ab9e17d1a446ab9cd9ed1f
RUN chown -R root:root /home/pyshell
RUN chmod -R 755 /home/pyshell

CMD ["/usr/sbin/xinetd","-dontfork"]
