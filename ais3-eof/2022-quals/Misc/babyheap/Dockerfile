FROM python:3.9

RUN apt-get update
RUN apt-get install xinetd -qy
RUN apt-get install wget zip cowsay -qy

RUN mv /usr/games/cowsay /usr/local/bin/cowsay

RUN useradd -m babyheap
COPY ./share /home/babyheap
COPY ./xinetd /etc/xinetd.d/babyheap
RUN chown -R root:root /home/babyheap
RUN chmod -R 755 /home/babyheap

RUN mkdir /tmp/sandbox/ && chmod 333 /tmp/sandbox/

RUN python -m pip install xonsh[full]

COPY ./flag/readflag.c /readflag.c
COPY ./flag/flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag

CMD ["/usr/sbin/xinetd","-dontfork"]
