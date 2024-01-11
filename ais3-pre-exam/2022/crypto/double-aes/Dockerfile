FROM python:3.10

RUN apt-get update && apt-get install socat -y
RUN pip install pycryptodome

WORKDIR /app
COPY chal.py .

RUN useradd -ms /bin/bash ctf
USER ctf
ENTRYPOINT ["socat", "TCP-LISTEN:7414,fork,reuseaddr", "EXEC:'python chal.py',stderr"]
