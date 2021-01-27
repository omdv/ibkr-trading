FROM python:3

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

ENV IB_GATEWAY_HOST=ib-gateway
ENV TRADING_MODE=paper
ENV CONDA_VERSION 4.7.12
ENV CONDA_HASH 79510c6e7bd9e012856e25dcb21b3e093aa4ac8113d9aa7e82a86987eabe1c31

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py37_$CONDA_VERSION-Linux-x86_64.sh -O ~/miniconda.sh && \
    echo "${CONDA_HASH}  Miniconda3-py37_$CONDA_VERSION-Linux-x86_64.sh" > miniconda.md5 && \
    if [ $(md5sum -c miniconda.md5 | awk '{print $2}') != "OK" ] ; then exit 1; fi && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

RUN conda update -y conda pip && \
    pip install --upgrade pip

RUN conda install -y -c conda-forge \
    jupyterlab=2.1.0

CMD ["jupyter","lab"]

# CMD ["python","/tmp/test.py"]

# COPY requirements.txt /tmp/
# RUN pip install -r /tmp/requirements.txt
# COPY ./test.py /tmp/
# CMD ["python","/tmp/test.py"]
