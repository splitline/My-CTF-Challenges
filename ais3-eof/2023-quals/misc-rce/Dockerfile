FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY ./app /app

RUN echo "FLAG{this_is_a_fake_flag}" > /flag
RUN chmod 0400 /flag && chown root:root /flag
