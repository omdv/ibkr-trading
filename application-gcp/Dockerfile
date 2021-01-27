FROM python:3

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

# Default ENV
ENV IB_GATEWAY_HOST=ib-gateway
ENV IB_GATEWAY_PORT=4041

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./app.py /tmp/
CMD ["python","/tmp/app.py"]
