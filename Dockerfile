# pulling official base image
FROM --platform=linux/amd64 python:3.10.2-slim-bullseye as python-base
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.2.2 \
    POETRY_HOME=/opt/poetry \
    WORKDIR_PATH=/app

ENV PATH="$POETRY_HOME/bin:$PATH"

#set working directory
WORKDIR $WORKDIR_PATH

FROM python-base as builder

RUN : \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
        netcat \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && :

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python

# copy project requirement files here to ensure they will be cached.
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry export -f requirements.txt --without-hashes -o requirements.txt \
    && poetry run pip install -r requirements.txt

# `production` image used for runtime
FROM python-base as production
ENV PATH="$WORKDIR_PATH/.venv/bin:$PATH"
COPY --from=builder $WORKDIR_PATH $WORKDIR_PATH
COPY src/ $WORKDIR_PATH
