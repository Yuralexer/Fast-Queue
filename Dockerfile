FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/pyenv/pyenv.git /root/.pyenv

ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

RUN bash -c "\
    pyenv install 3.12.0 && \
    pyenv global 3.12.0 && \
    curl -LsSf https://astral.sh/uv/install.sh | sh"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv && uv pip install -r pyproject.toml

COPY manage.py .
COPY testProProject ./testProProject
# Add paths to apps here
COPY auth_app ./auth_app

EXPOSE 8000

CMD ["uv", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]