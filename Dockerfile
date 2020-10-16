FROM debian:stretch
VOLUME /output
RUN apt-get update
# From https://github.com/openwall/john/blob/bleeding-jumbo/doc/INSTALL-UBUNTU#L26
RUN apt-get install git build-essential libssl-dev zlib1g-dev yasm pkg-config libgmp-dev libpcap-dev libbz2-dev -y
RUN git clone https://github.com/openwall/john -b bleeding-jumbo jtr
WORKDIR /jtr/src
RUN ./configure && make -s clean && make -sj4
WORKDIR /
COPY entrypoint.sh /entrypoint.sh
