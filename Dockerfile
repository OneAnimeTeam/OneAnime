FROM alpine:latest

ENV LANG C.UTF-8

WORKDIR /home/oneanime/

ENV LIBRARY_PATH=/lib:/usr/lib

RUN apk add --no-cache python3 zlib-dev freetype tiff tcl jpeg libwebp \
&& apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& pip3 install Pillow \
&& apk del --purge .build-deps
