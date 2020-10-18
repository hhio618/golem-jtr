#FROM debian:stretch
FROM golemfactory/base:1.8
RUN apt-get update
# From https://github.com/openwall/john/blob/bleeding-jumbo/doc/INSTALL-UBUNTU#L26
RUN apt-get install git build-essential libssl-dev zlib1g-dev yasm pkg-config libgmp-dev libpcap-dev libbz2-dev -y
WORKDIR /
RUN git clone https://github.com/openwall/john -b bleeding-jumbo jtr
WORKDIR /jtr/src
RUN ./configure && make -s clean && make -sj4
COPY entrypoint.sh /golem/entrypoints/
VOLUME /golem/work /golem/output /golem/resource
WORKDIR /golem/work
