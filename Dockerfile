FROM        python:3.9.7

COPY        ./requirements.txt /app/requirements.txt
WORKDIR     /app


RUN         python -m pip install -U pip           \
    && python -m pip install -r ./requirements.txt

COPY        . /app

CMD python -m yuganda
