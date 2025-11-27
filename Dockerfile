# --- Builder Stage ---
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ARG ENVIRONMENT

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy


COPY pyproject.toml uv.lock ./


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project $(if [ "$ENVIRONMENT" = 'production' ]; then echo '--no-dev'; fi)


COPY ./src /src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen $(if [ "$ENVIRONMENT" = 'production' ]; then echo '--no-dev'; fi) \
    && if [ "$ENVIRONMENT" = 'production' ]; then rm -rf /root/.cache/uv; fi

COPY ./src/entrypoint.sh /src/entrypoint.sh

# --- Runtime Stage ---
FROM python:3.13-slim-bookworm


RUN groupadd --system app && useradd --system --gid app --home /src app

ENV PATH="/.venv/bin:$PATH" \
    PYTHONPATH="/src/app" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime \
    && echo "Europe/Madrid" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

USER app
WORKDIR /src
COPY --from=builder --chown=app:app /src/entrypoint.sh /entrypoint.sh
COPY pyproject.toml /pyproject.toml

RUN chmod +x '/entrypoint.sh'

COPY --from=builder --chown=app:app ./src /src
COPY --from=builder --chown=app:app /.venv /.venv


CMD ["/entrypoint.sh"]