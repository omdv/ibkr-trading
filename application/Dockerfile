FROM python:3

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

# Default ENV
ENV IB_GATEWAY_HOST=ib-gateway
ENV TRADING_MODE=paper

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./test.py /tmp/
CMD ["python","/tmp/test.py"]
