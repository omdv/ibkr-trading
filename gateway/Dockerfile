FROM ubuntu:focal

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

RUN  apt-get update \
    && apt-get install -y wget unzip fail2ban socat cron supervisor xvfb \
    && apt-get install -y libxtst6 libxrender1 libxi6 \
    && apt-get install tini -y

# versions
ARG IBC_VERSION
ARG IB_GATEWAY_VERSION

# install IBC
RUN mkdir /opt/ibc
WORKDIR /opt/ibc/
RUN wget https://github.com/IbcAlpha/IBC/releases/download/${IBC_VERSION}/IBCLinux-${IBC_VERSION}.zip
RUN unzip IBCLinux-${IBC_VERSION}.zip

# install IB Gateway
RUN mkdir /opt/ibgateway
WORKDIR /opt/ibgateway
RUN wget https://download2.interactivebrokers.com/installers/ibgateway/stable-standalone/ibgateway-stable-standalone-linux-x64.sh
RUN chmod -R u+x *.sh
RUN (printf "/root/Jts/ibgateway/${IB_GATEWAY_VERSION}\nn" && cat) | /opt/ibgateway/ibgateway-stable-standalone-linux-x64.sh
RUN rm -rf /opt/ibgateway

# copy modified gateway scripts to use env variables
COPY ./gatewaystart.sh /opt/ibc/gatewaystart.sh
WORKDIR /opt/ibc/
RUN chmod u+x *.sh
RUN chmod u+x scripts/*.sh

# create folders and copy settings
RUN mkdir /root/ibc
COPY ./config.ini /root/ibc/config.ini

# # Overwrite vmoptions file
# RUN rm -f /root/Jts/ibgateway/${IB_GATEWAY_VERSION}/ibgateway.vmoptions
# COPY ./ibgateway.vmoptions /root/Jts/ibgateway/${IB_GATEWAY_VERSION}/ibgateway.vmoptions

# some default env
ENV TZ=America/Chicago
ENV DISPLAY :0

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# healthcheck - if gateway not running kill the container
HEALTHCHECK --start-period=30s --timeout=5s --interval=10s --retries=2 CMD bash -c 'pidof java || kill 1' || exit 1

# tini entrypoint to be able to `kill 1`
ENTRYPOINT ["tini", "--"]
CMD ["/usr/bin/supervisord"]
