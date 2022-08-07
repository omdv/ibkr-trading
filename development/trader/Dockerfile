FROM python:3.7

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

# Default ENV
ENV IB_GATEWAY_HOST=ib-gateway
ENV IB_GATEWAY_PORT=4041

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./app.py /tmp/

# Jupyter config with fixed password
COPY ./jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

CMD ["python","/tmp/app.py"]
# CMD ["jupyter-lab", "--allow-root"]
