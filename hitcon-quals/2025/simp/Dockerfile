FROM python:3.13.7

RUN apt-get update
RUN apt-get install xinetd -qy

RUN useradd -m ctf
COPY ./share /home/ctf
RUN chmod 1733 /tmp
RUN chown -R root:root /home/ctf
RUN chmod -R 755 /home/ctf

WORKDIR /home/ctf

COPY ./xinetd /etc/xinetd.d/chal
COPY flag /home/ctf/flag
RUN chmod 644 /home/ctf/flag

CMD ["/usr/sbin/xinetd","-dontfork"]