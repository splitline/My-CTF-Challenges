FROM python:3.10

RUN apt-get update
RUN apt-get install xinetd -qy
RUN useradd -m pyjail
COPY ./share /home/pyjail
COPY ./xinetd /etc/xinetd.d/pyjail
COPY ./flag /flag_secrettttttttt
RUN chown -R root:root /home/pyjail
RUN chmod -R 755 /home/pyjail

CMD ["/usr/sbin/xinetd","-dontfork"]
