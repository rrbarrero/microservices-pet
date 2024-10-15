FROM debian:bookworm-20240926-slim

ENV PATH="/code/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/" sh

WORKDIR /code

COPY . .

RUN uv sync
