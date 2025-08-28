FROM python:3.13-slim


RUN apt-get update && apt-get install -y gcc

WORKDIR /app
COPY app.py /app
COPY index.html /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY flag /flag
RUN chmod 0400 /flag
COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod 4755 /readflag

USER nobody

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--timeout=120", "app:app"]


