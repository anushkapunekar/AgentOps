#!/usr/bin/env bash
# simple startup: run uvicorn (default) - change for production
uvicorn app.main:app --host 0.0.0.0 --port 8000
