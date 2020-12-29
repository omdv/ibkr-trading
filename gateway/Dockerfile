FROM dorowu/ubuntu-desktop-lxde-vnc:focal

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

ARG IBCversion=3.8.3

RUN  apt-get update \
    && apt-get install -y wget unzip fail2ban socat

# install IBC
RUN mkdir /opt/ibc
WORKDIR /opt/ibc/
RUN wget https://github.com/IbcAlpha/IBC/releases/download/${IBCversion}/IBCLinux-${IBCversion}.zip
RUN unzip IBCLinux-${IBCversion}.zip

# copy modified gateway scripts to use env variables
COPY ./gatewaystart.sh /opt/ibc/gatewaystart.sh
RUN chmod u+x *.sh
RUN chmod u+x scripts/*.sh

# install IB Gateway
RUN mkdir /opt/ibgateway
WORKDIR /opt/ibgateway
RUN wget https://download2.interactivebrokers.com/installers/ibgateway/stable-standalone/ibgateway-stable-standalone-linux-x64.sh
RUN chmod -R u+x *.sh
RUN yes n | /opt/ibgateway/ibgateway-stable-standalone-linux-x64.sh
RUN rm -rf /opt/ibgateway

# create folders and copy settings
RUN mkdir /root/ibc
COPY ./config.ini /root/ibc/config.ini

# startup scripts
COPY ./runscript.sh /opt/runscript.sh
RUN chmod +x /opt/runscript.sh