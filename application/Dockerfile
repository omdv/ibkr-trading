FROM python:3

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./test.py /tmp/
CMD ["python","/tmp/test.py"]