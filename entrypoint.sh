#!/bin/sh

uv run python seed.py
exec uv run uwsgi --ini uwsgi.ini
