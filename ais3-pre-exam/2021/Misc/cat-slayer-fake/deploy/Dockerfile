FROM python:3.8

RUN apt update
RUN apt install ssh -qy
RUN mkdir /run/sshd

RUN adduser --disabled-password --gecos "" --shell /home/h173/lock.py h173
RUN sed -i -re 's/^h173:[^:]+:/h173::/' /etc/passwd /etc/shadow
RUN touch /home/h173/.hushlogin

COPY ./ssh/sshd_config /etc/ssh/sshd_config
COPY ./ssh/sshd /etc/pam.d/sshd

CMD ["/usr/sbin/sshd", "-D"]