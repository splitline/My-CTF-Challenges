FROM julia:1.7.2-bullseye

RUN apt-get update && apt-get install nginx apache2-utils -y && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash web

USER web
RUN julia -e 'import Pkg;Pkg.add(Pkg.PackageSpec(;name="Genie", version="4.14.0"))'

USER root
RUN mkdir /app
WORKDIR /app
RUN mkdir uploads
COPY main.jl .
COPY flag.txt .
RUN mv flag.txt flag-$(md5sum flag.txt | cut -d ' ' -f 1 | tr -d '\n').txt

COPY default.conf /etc/nginx/sites-available/default
COPY start.sh .

RUN chown -R web:web .

CMD ["timeout", "600", "./start.sh"]
