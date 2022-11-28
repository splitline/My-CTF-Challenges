FROM python:3.9.13@sha256:d0228a84a4ed50a620d1dc5d38aae226db6608d6bd2c9816592823cd73bf4ad9

RUN apt-get update
RUN apt-get install xinetd -qy

RUN useradd -m ctf
COPY ./share /home/ctf
RUN chown -R root:root /home/ctf
RUN chmod -R 755 /home/ctf

WORKDIR /home/ctf

COPY ./xinetd /etc/xinetd.d/chal
RUN echo 'hitcon{PaIn pAiN PAin PiCkLe QAq!}' > /home/ctf/flag

CMD ["/usr/sbin/xinetd","-dontfork"]
