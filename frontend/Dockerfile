# Wheels Directory for Distro and its Dependencies (aka requirements)
ARG DISTRO_WHEELS=/app/dist
# https://docs.docker.com/build/building/variables/#scoping

# can be ovveriden by --build-arg PYTHON_TAG=3.11.12
ARG PY_VERSION=3.11.12
FROM python:${PY_VERSION}-alpine AS python_alpine



FROM python_alpine AS builder

COPY uv.lock pyproject.toml ./

# Install uv
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

# Export Exact/Pinned Prod (install only) dependencies, into pip format
FROM builder AS prod_builder
RUN uv export --no-dev --frozen --no-emit-project -f requirements-txt -o requirements.txt


#### PLACE SOURCE FILES - STAGE ####
FROM scratch as source

WORKDIR /app

COPY --from=prod_builder requirements.txt .
# Copy Source Code
# COPY . .
# COPY app.py .
COPY pyproject.toml .
COPY uv.lock .
# COPY LICENSE .
# COPY README.md .


###### BUILD WHEELS from Sources - STAGE ######
FROM python_alpine AS build_wheels
ARG DISTRO_WHEELS

# Essential build tools
RUN apk update && \
    apk add --no-cache build-base && \
    pip install -U pip && \
    rm -rf /var/cache/apk/*

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
# RUN uv build --wheel --out-dir "/tmp/build-wheels" && \
#     mkdir -p "${DISTRO_WHEELS}" && \
#     find /tmp/build-wheels -name "*.whl" -exec mv {} "${DISTRO_WHEELS}" \;

# Now runtime required wheels are in DISTRO_WHEELS folder




###### INSTALL WHEELS into env - STAGE ######
FROM python_alpine AS install
ARG DISTRO_WHEELS

# If at runtime our app needs external packages, do apk install here
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends git && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

WORKDIR /app

# we copy the wheels built in 'build_wheels' stage
COPY --from=build_wheels ${DISTRO_WHEELS} dist

# Install wheels for our Distro and its Install/Runtime Dependencies
# in user site-packages (ie /root/.local/lib/python3.11/site-packages)
RUN pip install --no-deps --no-cache-dir --user ./dist/*.whl




## PROD - Leaf STAGE ##

FROM install AS prod

# Add user's bin folder, to PATH to make biskotakigold CLI available
ENV PATH="/root/.local/bin:$PATH"

# Expose the frontend port
EXPOSE 8501

# Command to run the Streamlit app
# CMD ["streamlit", "run", "app.py"]
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# --server.address TEXT           The address where the server will listen for
# client and browser connections.

# Use this if you want to bind the server to a
# specific address. If set, the server will
# only be accessible from this address, and
# not from any aliases (like localhost).

# Default: (unset)  [env var:
# STREAMLIT_SERVER_ADDRESS]
# --server.port INTEGER           The port where the server will listen for
# browser connections.  [env var:
# STREAMLIT_SERVER_PORT]


# --browser.serverAddress TEXT    Internet address where users should point
# their browsers in order to connect to the
# app. Can be IP address or DNS name and path.


# --browser.serverAddress TEXT    Internet address where users should point
# their browsers in order to connect to the
# app. Can be IP address or DNS name and path.

