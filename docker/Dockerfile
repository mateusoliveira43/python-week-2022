ARG PROJECT_NAME=beerlog
ARG WORK_DIR=/home/$PROJECT_NAME/$PROJECT_NAME
ARG GROUP_ID=1000
ARG USER_ID=1000
ARG PYTHON_VERSION=3.8.13
ARG POETRY_VERSION=1.1.13

FROM python:$PYTHON_VERSION as base
ARG PROJECT_NAME
ARG WORK_DIR
ARG GROUP_ID
ARG USER_ID

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH=/home/$PROJECT_NAME/.local/bin:$PATH

RUN groupadd --gid $GROUP_ID $PROJECT_NAME \
    && useradd --uid $USER_ID --gid $GROUP_ID --create-home $PROJECT_NAME
USER $PROJECT_NAME
RUN mkdir "$WORK_DIR"
WORKDIR $WORK_DIR

FROM base as setup
ARG PROJECT_NAME
ARG POETRY_VERSION

ENV POETRY_VERSION=$POETRY_VERSION \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
COPY ./poetry.lock ./pyproject.toml ./
COPY ./$PROJECT_NAME ./$PROJECT_NAME

FROM setup as development

RUN poetry install

FROM setup as build

RUN poetry build --format wheel \
    && poetry export --format requirements.txt --output constraints.txt --without-hashes

FROM base as production
ARG PROJECT_NAME
ARG WORK_DIR

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

COPY --from=build $WORK_DIR/dist/*.whl ./
COPY --from=build $WORK_DIR/constraints.txt ./

RUN pip install --no-cache-dir ./$PROJECT_NAME*.whl --constraint constraints.txt
