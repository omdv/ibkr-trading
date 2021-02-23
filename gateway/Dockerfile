FROM ubuntu:focal

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

# IBC version to use
ARG IBCversion=3.8.4-beta.2
ARG IBGateway_version=978

RUN  apt-get update \
    && apt-get install -y wget unzip fail2ban socat cron supervisor xvfb \
    && apt-get install -y libxtst6 libxrender1 libxi6 \
    && apt-get install tini -y

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

# Overwrite vmoptions file
RUN rm -f /root/Jts/ibgateway/${IBGateway_version}/ibgateway.vmoptions
COPY ./ibgateway.vmoptions /root/Jts/ibgateway/${IBGateway_version}/ibgateway.vmoptions

# default env
ENV TWS_MAJOR_VRSN=${IBGateway_version}
ENV TZ=America/Chicago
ENV IBC_INI=/root/ibc/config.ini
ENV IBC_PATH=/opt/ibc
ENV LOG_PATH=/root/ibc/Logs
ENV JAVA_PATH=/opt/i4j_jres/1.8.0_152-tzdata2019c/bin
ENV TWS_PATH=/root/Jts/
ENV FIXUSERID=
ENV FIXPASSWORD=
ENV DISPLAY :0

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# healthcheck - if gateway not running kill the container
HEALTHCHECK --start-period=30s --timeout=5s --interval=10s --retries=2 CMD bash -c 'pidof java || kill 1' || exit 1

# tini entrypoint to be able to `kill 1`
ENTRYPOINT ["tini", "--"]
CMD ["/usr/bin/supervisord"]