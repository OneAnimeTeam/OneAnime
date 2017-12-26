FROM alpine:latest

ENV LANG C.UTF-8

WORKDIR /home/oneanime/

ENV LIBRARY_PATH=/lib:/usr/lib

RUN sed -i s/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g /etc/apk/repositories \
&& apk add --no-cache python3 zlib-dev jpeg-dev libwebp \
&& apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& pip3 install Pillow -i https://mirrors.ustc.edu.cn/pypi/web/simple \
&& apk del --purge .build-deps
