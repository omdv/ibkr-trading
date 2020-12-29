FROM python:3

# Default ENV
ENV IB_GATEWAY_URLNAME=ib-gateway
ENV IB_GATEWAY_URLPORT=4000
ENV MKT_DATA_TYPE=4

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./test.py /tmp/
CMD ["python","/tmp/test.py"]