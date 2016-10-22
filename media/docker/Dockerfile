FROM debian:sid

ENV DEBIAN_FRONTEND noninteractive

RUN echo CACHEBUST 1

RUN apt-get update && apt-get dist-upgrade --yes
RUN apt-get install --yes --install-recommends diffoscope
