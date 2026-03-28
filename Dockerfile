FROM python:3.13-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN echo "deb http://debian.parspack.com/debian/ bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://debian.parspack.com/debian/ bookworm main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://debian.parspack.com/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://debian.parspack.com/debian/ bookworm-proposed-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://debian.parspack.com/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb-src http://debian.parspack.com/debian/ bookworm-proposed-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

