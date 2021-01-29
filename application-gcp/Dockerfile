FROM python:3.7

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

# Default ENV
ENV IB_GATEWAY_HOST=ib-gateway
ENV IB_GATEWAY_PORT=4041

# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./app.py /tmp/

CMD ["python","/tmp/app.py"]
