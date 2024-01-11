FROM mcr.microsoft.com/azure-sql-edge:latest

USER root
RUN wget "https://github.com/microsoft/go-sqlcmd/releases/download/v0.6.0/sqlcmd-v0.6.0-linux-$(arch).tar.bz2" -O /tmp/sqlcmd.tar.bz2 && \
    tar -xjf /tmp/sqlcmd.tar.bz2 -C /usr/local/bin && \
    rm /tmp/sqlcmd.tar.bz2

USER mssql
COPY init.sql /init.sql
COPY init.sh /init.sh
COPY entrypoint.sh /entrypoint.sh

CMD /bin/bash ./entrypoint.sh

ENV PATH="/opt/mssql-tools/bin:${PATH}"
