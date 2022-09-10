FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache: \
  && /usr/local/bin/python -m pip install --upgrade pip \
  && pip3 install poetry && echo "Poetry installed successfully"

# set work directory
WORKDIR /app
RUN mkdir logs

COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --without dev

COPY . /app/
