FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg xvfb xauth fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
