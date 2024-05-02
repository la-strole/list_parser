FROM python:slim-bullseye

# Copy files and virtual environments (be sure to not include .env file with tokens)
ADD ./pyproject.toml /home

RUN apt update

# Install make
RUN apt install make

# Install curl
RUN apt install curl -y

WORKDIR /home
# Install environment
# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install poetry dependencies
RUN ~/.local/bin/poetry config virtualenvs.create false \ 
    && ~/.local/bin/poetry install --no-root --without dev

ADD ./ /home/list_parser

WORKDIR /home/list_parser
