# ===============================
# Dockerfile.builder
# ===============================
FROM python:3.12-slim AS builder

# -------------------------------
# Установка системных зависимостей
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ make cmake python3-dev \
    libffi-dev libssl-dev zlib1g-dev libbz2-dev \
    liblzma-dev libreadline-dev libsqlite3-dev libncurses-dev \
    wget curl git ca-certificates pkg-config libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Установка Rust
# -------------------------------
ENV HOME=/root
ENV PATH="$HOME/.rust/usr/local/bin:$PATH"

RUN set -eux; \
    mkdir -p $HOME/.rust; \
    cd $HOME/.rust; \
    curl -LO https://static.rust-lang.org/dist/rust-1.90.0-aarch64-unknown-linux-gnu.tar.xz; \
    tar -xvf rust-1.90.0-aarch64-unknown-linux-gnu.tar.xz; \
    cd rust-1.90.0-aarch64-unknown-linux-gnu; \
    ./install.sh --destdir="$HOME/.rust" --components=rustc,cargo,rust-std-aarch64-unknown-linux-gnu; \
    export PATH="$HOME/.rust/usr/local/bin:$PATH"; \
    rustc --version; \
    cargo --version

ENV PATH="$HOME/.rust/usr/local/bin:$PATH"

# -------------------------------
# Оптимизации сборки
# -------------------------------
ENV CFLAGS="-O3 -march=native -pipe -fomit-frame-pointer -flto"
ENV CXXFLAGS="${CFLAGS}"
ENV LDFLAGS="-Wl,-O1,--as-needed,-flto,-s"
ENV RUSTFLAGS="-C target-cpu=native -C embed-bitcode=yes -C opt-level=3 -C lto=fat -C codegen-units=1 -C strip=symbols"
ENV CARGO_PROFILE_RELEASE_LTO=true
ENV CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
ENV CARGO_PROFILE_RELEASE_STRIP=symbols
ENV MAKEFLAGS="-j$(nproc)"
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/lib/pkgconfig"

# -------------------------------
# Установка uv
# -------------------------------
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# -------------------------------
# Настройки uv и кэширования
# -------------------------------
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/root/.cache/uv
ENV UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# -------------------------------
# Предварительная установка зависимостей Python (кэшируем)
# -------------------------------
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable

# -------------------------------
# Образ builder готов
# -------------------------------
