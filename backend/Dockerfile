FROM python:3.12.4-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential curl gnupg2 \
    # dependencies for fetching Python packages
    && apt-get install -y git openssh-client \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    && apt-get install -y ca-certificates \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# [HACK] deactivate ssl cert checking for pypi, files.py, files.pythonhosted and pypi.python to install package via pip
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"

# Install poetry using pip
RUN pip install --upgrade setuptools
RUN pip install poetry

RUN git config --global http.sslVerify false

# move poetry related file to current directory
COPY poetry.lock ./
COPY pyproject.toml ./

# [HACK] deactivate ssl cert checking for pypi, files.py, files.pythonhosted and pypi.python to install package via poetry
RUN poetry config certificates.PyPI.cert false
RUN poetry config repositories.FPHO https://files.pythonhosted.org
RUN poetry config certificates.FPHO.cert false

COPY ./ ./

# Install package using poetry
RUN poetry install

# Start celery worker
RUN chmod +x worker-entrypoint.sh