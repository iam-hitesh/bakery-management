FROM postgres:12-alpine

COPY ./postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin && rm -rf /usr/local/bin/maintenance