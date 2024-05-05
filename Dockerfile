FROM postgres:12.15-alpine

COPY startup.sql /docker-entrypoint-initdb.d/
