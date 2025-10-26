# ===============================
# Stage 1: Builder
# ===============================
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ make cmake python3-dev \
    libffi-dev libssl-dev zlib1g-dev libbz2-dev \
    liblzma-dev libreadline-dev libsqlite3-dev libncurses-dev \
    wget curl git ca-certificates pkg-config libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------- Rust -----------------
ENV HOME=/root
ENV PATH="$HOME/.rust/usr/local/bin:$PATH"
RUN set -eux; \
    rm -rf $HOME/.rust rust.tar.xz; \
    mkdir -p $HOME/.rust; \
    cd $HOME/.rust; \
    curl -LO https://static.rust-lang.org/dist/rust-1.90.0-aarch64-unknown-linux-gnu.tar.xz; \
    ls -lh rust-1.90.0-aarch64-unknown-linux-gnu.tar.xz; \
    tar -xvf rust-1.90.0-aarch64-unknown-linux-gnu.tar.xz; \
    cd rust-1.90.0-aarch64-unknown-linux-gnu; \
    ./install.sh --destdir="$HOME/.rust" --components=rustc,cargo,rust-std-aarch64-unknown-linux-gnu; \
    cd ..; \
    export PATH="$HOME/.rust/usr/local/bin:$PATH"; \
    rustc --version; \
    cargo --version

ENV PATH="$HOME/.rust/usr/local/bin:$PATH"

# ----------------- Оптимизации сборки -----------------
# CFLAGS — флаги компилятора для C
# Варианты:
#   -O0, -O1, -O2, -O3         (уровень оптимизации, 3 — максимальная)
#   -march=native               (оптимизация под текущий CPU)
#   -pipe                       (ускорение через пайпы вместо временных файлов)
#   -fomit-frame-pointer        (не сохранять FP для ускорения)
#   -flto                       (Link Time Optimization)
ENV CFLAGS="-O3 -march=native -pipe -fomit-frame-pointer -flto"

# CXXFLAGS — флаги компилятора для C++
# Обычно наследует CFLAGS, но можно добавить свои специфичные для C++
ENV CXXFLAGS="${CFLAGS}"

# LDFLAGS — флаги линковщика
# Варианты:
#   -Wl,-O1                    (оптимизация линковки)
#   --as-needed                 (не подключать лишние библиотеки)
#   -flto                       (Link Time Optimization)
#   -s                          (удаление символов для уменьшения размера бинарника)
ENV LDFLAGS="-Wl,-O1,--as-needed,-flto,-s"

# RUSTFLAGS — флаги компиляции Rust
# Варианты:
#   -C opt-level=0..3           (уровень оптимизации, 3 — максимальный)
#   -C target-cpu=native        (оптимизация под текущий CPU)
#   -C lto=fat                  (Link Time Optimization, fat/lto/false)
#   -C codegen-units=1..16      (количество единиц генерации кода)
#   -C strip=symbols            (удаление символов для уменьшения размера)
ENV RUSTFLAGS="-C target-cpu=native -C embed-bitcode=yes -C opt-level=3 -C lto=fat -C codegen-units=1 -C strip=symbols"

# CARGO_PROFILE_RELEASE_* — тонкая настройка профиля release в Cargo
# LTO=true — включить Link Time Optimization
# CODEGEN_UNITS=1 — уменьшить распараллеливание для максимальной оптимизации
# STRIP=symbols — удалить символы из релизного бинарника
ENV CARGO_PROFILE_RELEASE_LTO=true
ENV CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
ENV CARGO_PROFILE_RELEASE_STRIP=symbols

# MAKEFLAGS — параметры для make, ускоряют сборку на многоядерных системах
# Варианты:
#   -jN — количество потоков сборки (обычно nproc)
ENV MAKEFLAGS="-j$(nproc)"

# PKG_CONFIG_PATH — путь поиска .pc файлов для pkg-config
# Варианты: пути, где установлены библиотеки, чтобы корректно находились заголовки и либы
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/lib/pkgconfig"

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Рабочая директория
WORKDIR /app

# # Настройки uv и кэширования

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/root/.cache/uv
ENV UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# -------------------------------
# 1) Устанавливаем зависимости без проекта (кэшируем)
# -------------------------------

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable 
# -------------------------------
# 2) Копируем проект в контейнер
# -------------------------------
ADD . /app

# -------------------------------
# 3) Финальная синхронизация проекта
# -------------------------------
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# ===============================
# Stage 2: Runtime
# ===============================
FROM python:3.12-slim

WORKDIR /app

# Копируем только виртуальное окружение из builder
COPY --from=builder /app/.venv /app/.venv

# Копируем код приложения (если нужен для uv run или прямого запуска)
COPY --from=builder /app /app

# Порт приложения (если FastAPI)
EXPOSE 8000

# Команда запуска
CMD ["/app/.venv/bin/python", "-m", "app.main"]
