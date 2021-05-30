FROM python:3.8

RUN apt-get update
RUN apt-get install xinetd -qy

RUN useradd --no-create-home --home-dir / --shell /bin/false sandbox

COPY ./share /game
COPY ./xinetd /etc/xinetd.d/game
COPY ./flag /secr3t_flag_meow_meow
RUN chown -R root:root /game
RUN chmod -R 700 /game
RUN chmod 755 /game

RUN chown sandbox:sandbox /game/sandbox.py
RUN chmod 4755 /game/sandbox.py

CMD ["/usr/sbin/xinetd","-dontfork"]