# Wheels Directory for Distro and its Dependencies (aka requirements)
ARG DISTRO_WHEELS=/app/dist
# https://docs.docker.com/build/building/variables/#scoping

# ARG PY_VERSION=3.11.12
# FROM python:${PY_VERSION}-alpine AS python_alpine
ARG PY_VERSION=3.12.9
# can be ovveriden by --build-arg PYTHON_TAG=3.11.12
FROM python:${PY_VERSION}-slim-bullseye as python_slim



FROM python_slim AS builder

COPY uv.lock pyproject.toml ./

# Install uv
# RUN python -m pip install uv

# RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

# Export Exact/Pinned Prod (install only) dependencies, into pip format
FROM builder AS prod_builder
RUN uv export --no-dev --frozen --no-emit-project -f requirements-txt -o requirements.txt
# Export Exact/Pinned Prod + Test dependencies, into pip format
FROM builder AS test_builder
RUN uv export --no-dev --frozen --no-emit-project --extra test -f requirements-txt -o requirements.txt
# Export Exact/Pinned Prod + Alembic dependencies, into pip format
FROM builder AS alembic_deps
RUN uv export --no-dev --frozen --no-emit-project --extra migrations -f requirements-txt -o requirements.txt



#### PLACE SOURCE FILES - STAGE ####
FROM scratch as source
WORKDIR /app
COPY --from=prod_builder requirements.txt .
# Copy Source Code
COPY src src
COPY pyproject.toml .
COPY uv.lock .
# COPY LICENSE .
COPY README.md .


###### BUILD WHEELS from Sources - STAGE ######
FROM python_slim AS build_wheels
ARG DISTRO_WHEELS

# Essential build tools
# RUN apk update && \
#     apk add --no-cache build-base && \
#     pip install -U pip && \
#     rm -rf /var/cache/apk/*

# Essential build-time dependencies
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir poetry-core && \
#     pip install --no-cache-dir build

WORKDIR /app
COPY --from=source /app .

# Build Wheels for Distro's Dependencies, from /app/requirements.txt file
RUN pip wheel --wheel-dir "${DISTRO_WHEELS}" -r ./requirements.txt

# Build Wheels for Distro's (own) Package
RUN uv build --wheel --out-dir "/tmp/build-wheels" && \
    mkdir -p "${DISTRO_WHEELS}" && \
    find /tmp/build-wheels -name "*.whl" -exec mv {} "${DISTRO_WHEELS}" \;

# Now runtime required wheels are in DISTRO_WHEELS folder



###### INSTALL ALEMBIC ENV - STAGE ######
FROM python_slim AS alembic

COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

ARG DISTRO_WHEELS
WORKDIR /app

COPY --from=alembic_deps requirements.txt .

# Build Wheels for Distro's Dependencies, from /app/requirements.txt file
RUN pip wheel --wheel-dir "${DISTRO_WHEELS}" -r ./requirements.txt

# Copy Sources
COPY src src
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .

# Build Wheels for Distro's (own) Package
RUN uv build --wheel --out-dir "/tmp/build-wheels" && \
    mkdir -p "${DISTRO_WHEELS}" && \
    find /tmp/build-wheels -name "*.whl" -exec mv {} "${DISTRO_WHEELS}" \;

# Install wheels for our Distro and its Install/Runtime Dependencies
# in user site-packages (ie /root/.local/lib/python3.11/site-packages)
RUN pip install --no-deps --no-cache-dir --user "${DISTRO_WHEELS}"/*.whl

# Add user's bin folder, to PATH to make biskotakigold CLI available
ENV PATH="/root/.local/bin:$PATH"



###### INSTALL WHEELS into env - STAGE ######
FROM python_slim AS install
ARG DISTRO_WHEELS

# If at runtime our app needs external packages, do apk install here
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends git && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

WORKDIR /app

## prod version ##
# # we copy the wheels built in 'build_wheels' stage
# COPY --from=build_wheels ${DISTRO_WHEELS} dist

# # Install wheels for our Distro and its Install/Runtime Dependencies
# # in user site-packages (ie /root/.local/lib/python3.11/site-packages)
# RUN pip install --no-deps --no-cache-dir --user ./dist/*.whl


## poc version ##
COPY src src
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
RUN pip install .


## Image for TEST ##
FROM python_slim AS test
WORKDIR /app
## poc version ##
COPY src src
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
RUN pip install .[test]


# Add user's bin folder, to PATH to make biskotakigold CLI available
ENV PATH="/root/.local/bin:$PATH"


ENTRYPOINT [ "pytest" ]


## Image for PROD ##

FROM install AS prod

# Add user's bin folder, to PATH to make biskotakigold CLI available
ENV PATH="/root/.local/bin:$PATH"

# Expose the backend port
EXPOSE 8000
CMD ["-m", "okr_api.run_server"]

ENTRYPOINT [ "python" ]
