FROM python:3.10-slim

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

# Default ENV
ENV IB_GATEWAY_HOST=ib-gateway
ENV IB_GATEWAY_PORT=4041
ENV STORAGE_BACKEND=local

RUN apt-get update && apt-get install tini -y

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./app.py /tmp/

# healthcheck
HEALTHCHECK --start-period=30s --timeout=5s --interval=10s --retries=2 CMD bash -c 'pidof python || kill 1' || exit 1

# tini entrypoint to be able to `kill 1`
ENTRYPOINT ["tini", "--"]
CMD ["python", "/tmp/app.py"]
