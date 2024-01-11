FROM python:3.10

RUN chmod 1733 /tmp

RUN pip install --no-cache-dir bottle gunicorn

RUN apt update && apt install -y --no-install-recommends nginx

CMD ["bash", "/start.sh"]
