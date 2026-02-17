FROM ghcr.io/astral-sh/uv:python3.13-alpine
WORKDIR /app
ENV UV_NO_DEV=1
COPY api.py seed.py index.html favicon.ico uwsgi.ini uv.lock pyproject.toml entrypoint.sh /app/
RUN uv sync --locked
EXPOSE 10013
CMD ["./entrypoint.sh"]
