
FROM python:3.9

# I don't know why but only NTU mirror can install sid package of chromium
RUN sed -i 's/deb.debian.org/debian.csie.ntu.edu.tw/' /etc/apt/sources.list
RUN sed -i 's/security.debian.org/debian.csie.ntu.edu.tw/' /etc/apt/sources.list

RUN apt update && \
    apt install -y --no-install-recommends chromium-driver redis-server

# Install latest chromium, I don't want this challenge become a browser pwn challenge
RUN sed -i 's/bullseye /sid /' /etc/apt/sources.list
RUN apt update && \
    apt install -y --no-install-recommends chromium

RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir selenium redis rq

COPY xssbot.py /xssbot.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

RUN useradd --no-create-home --home-dir / --shell /bin/false user
CMD bash /run.sh