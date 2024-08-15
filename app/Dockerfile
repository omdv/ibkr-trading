FROM python:3.11-slim

LABEL maintainer="Oleg Medvedev <omdv.public@gmail.com>"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

CMD ["python", "-u", "/code/app/main.py"]
