FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

RUN useradd app -U
RUN mkdir -p /home/app
RUN chown app:app /home/app
WORKDIR /home/app/src

RUN apt-get update
RUN apt-get install netcat -y

USER app
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN /home/app/.poetry/bin/poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
RUN /home/app/.poetry/bin/poetry install

USER root
COPY . .
RUN chown -R app:app .
USER app

ENTRYPOINT ["/home/app/src/entrypoint.sh"]
