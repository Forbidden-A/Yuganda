FROM      python:3.9


COPY      ./requirements.txt /bot/requirements.txt
WORKDIR   /bot


RUN       python -m pip install -U pip                 \
    && python -m pip install -r ./requirements.txt

COPY      . /bot

CMD       python -m yuganda
# CMD       python -O -m yuganda